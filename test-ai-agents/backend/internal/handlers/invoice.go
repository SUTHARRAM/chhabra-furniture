package handlers

import (
    "bytes"
    "context"
    "fmt"
    "math/rand"
    "net/http"
    "time"

    "github.com/gin-gonic/gin"
    "github.com/jung-kurt/gofpdf"
    "github.com/yourorg/invoice-app/backend/internal/db"
    "github.com/yourorg/invoice-app/backend/internal/models"
    "go.mongodb.org/mongo-driver/bson"
    "go.mongodb.org/mongo-driver/bson/primitive"
    "go.mongodb.org/mongo-driver/mongo/options"
)

type InvoiceHandler struct{}

func NewInvoiceHandler() *InvoiceHandler { return &InvoiceHandler{} }

func generateInvoiceID() string {
    return fmt.Sprintf("INV-%s-%04d", time.Now().Format("20060102"), rand.Intn(10000))
}

func computeTotals(items []models.InvoiceItem) (subtotal, taxTotal, total float64) {
    for _, it := range items {
        line := it.Quantity * it.UnitPrice
        tax := line * it.TaxRate / 100.0
        subtotal += line
        taxTotal += tax
    }
    total = subtotal + taxTotal
    return
}

// Create
func (h *InvoiceHandler) Create(c *gin.Context) {
    var inv models.Invoice
    if err := c.ShouldBindJSON(&inv); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    inv.ID = primitive.NilObjectID
    if inv.InvoiceID == "" {
        inv.InvoiceID = generateInvoiceID()
    }
    inv.Subtotal, inv.TaxTotal, inv.Total = computeTotals(inv.Items)
    inv.Status = "draft"
    now := time.Now()
    inv.CreatedAt = now
    inv.UpdatedAt = now

    ctx, cancel := context.WithTimeout(c.Request.Context(), 5*time.Second)
    defer cancel()
    col := db.DB().Collection("invoices")
    res, err := col.InsertOne(ctx, inv)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to create invoice"})
        return
    }
    inv.ID = res.InsertedID.(primitive.ObjectID)
    c.JSON(http.StatusCreated, inv)
}

// List with optional date range (?from=YYYY-MM-DD&to=YYYY-MM-DD)
func (h *InvoiceHandler) List(c *gin.Context) {
    filter := bson.M{}
    from := c.Query("from")
    to := c.Query("to")
    if from != "" || to != "" {
        dateFilter := bson.M{}
        if from != "" {
            if t, err := time.Parse("2006-01-02", from); err == nil {
                dateFilter["$gte"] = t
            }
        }
        if to != "" {
            if t, err := time.Parse("2006-01-02", to); err == nil {
                // include end-of-day
                dateFilter["$lte"] = t.Add(24*time.Hour - time.Nanosecond)
            }
        }
        if len(dateFilter) > 0 {
            filter["created_at"] = dateFilter
        }
    }
    ctx, cancel := context.WithTimeout(c.Request.Context(), 10*time.Second)
    defer cancel()
    col := db.DB().Collection("invoices")
    cur, err := col.Find(ctx, filter, options.Find().SetSort(bson.D{{Key: "created_at", Value: -1}}))
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to fetch invoices"})
        return
    }
    defer cur.Close(ctx)
    var out []models.Invoice
    for cur.Next(ctx) {
        var inv models.Invoice
        if err := cur.Decode(&inv); err == nil {
            out = append(out, inv)
        }
    }
    c.JSON(http.StatusOK, out)
}

// Get by id (Mongo ObjectID or invoiceId)
func (h *InvoiceHandler) Get(c *gin.Context) {
    id := c.Param("id")
    filter := bson.M{}
    if oid, err := primitive.ObjectIDFromHex(id); err == nil {
        filter["_id"] = oid
    } else {
        filter["invoice_id"] = id
    }
    ctx, cancel := context.WithTimeout(c.Request.Context(), 5*time.Second)
    defer cancel()
    col := db.DB().Collection("invoices")
    var inv models.Invoice
    if err := col.FindOne(ctx, filter).Decode(&inv); err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "invoice not found"})
        return
    }
    c.JSON(http.StatusOK, inv)
}

// Update
func (h *InvoiceHandler) Update(c *gin.Context) {
    id := c.Param("id")
    var payload models.Invoice
    if err := c.ShouldBindJSON(&payload); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    payload.Subtotal, payload.TaxTotal, payload.Total = computeTotals(payload.Items)
    payload.UpdatedAt = time.Now()

    filter := bson.M{}
    if oid, err := primitive.ObjectIDFromHex(id); err == nil {
        filter["_id"] = oid
    } else {
        filter["invoice_id"] = id
    }

    update := bson.M{"$set": bson.M{
        "client_name":  payload.ClientName,
        "client_email": payload.ClientEmail,
        "client_phone": payload.ClientPhone,
        "items":        payload.Items,
        "subtotal":     payload.Subtotal,
        "tax_total":    payload.TaxTotal,
        "total":        payload.Total,
        "status":       payload.Status,
        "updated_at":   payload.UpdatedAt,
    }}

    ctx, cancel := context.WithTimeout(c.Request.Context(), 5*time.Second)
    defer cancel()
    col := db.DB().Collection("invoices")
    res := col.FindOneAndUpdate(ctx, filter, update, options.FindOneAndUpdate().SetReturnDocument(options.After))
    var updated models.Invoice
    if err := res.Decode(&updated); err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "invoice not found"})
        return
    }
    c.JSON(http.StatusOK, updated)
}

// Delete
func (h *InvoiceHandler) Delete(c *gin.Context) {
    id := c.Param("id")
    filter := bson.M{}
    if oid, err := primitive.ObjectIDFromHex(id); err == nil {
        filter["_id"] = oid
    } else {
        filter["invoice_id"] = id
    }
    ctx, cancel := context.WithTimeout(c.Request.Context(), 5*time.Second)
    defer cancel()
    col := db.DB().Collection("invoices")
    res, err := col.DeleteOne(ctx, filter)
    if err != nil || res.DeletedCount == 0 {
        c.JSON(http.StatusNotFound, gin.H{"error": "invoice not found"})
        return
    }
    c.Status(http.StatusNoContent)
}

// PDF export
func (h *InvoiceHandler) ExportPDF(c *gin.Context) {
    id := c.Param("id")
    filter := bson.M{}
    if oid, err := primitive.ObjectIDFromHex(id); err == nil {
        filter["_id"] = oid
    } else {
        filter["invoice_id"] = id
    }
    ctx, cancel := context.WithTimeout(c.Request.Context(), 5*time.Second)
    defer cancel()
    col := db.DB().Collection("invoices")
    var inv models.Invoice
    if err := col.FindOne(ctx, filter).Decode(&inv); err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "invoice not found"})
        return
    }

    pdf := gofpdf.New("P", "mm", "A4", "")
    pdf.AddPage()
    pdf.SetFont("Arial", "B", 16)
    pdf.Cell(40, 10, "Invoice "+inv.InvoiceID)
    pdf.Ln(12)
    pdf.SetFont("Arial", "", 12)
    pdf.Cell(40, 8, "Client: "+inv.ClientName)
    pdf.Ln(8)
    pdf.Cell(40, 8, fmt.Sprintf("Date: %s", inv.CreatedAt.Format("2006-01-02")))
    pdf.Ln(10)

    pdf.SetFont("Arial", "B", 12)
    pdf.CellFormat(80, 8, "Description", "1", 0, "L", false, 0, "")
    pdf.CellFormat(30, 8, "Qty", "1", 0, "C", false, 0, "")
    pdf.CellFormat(40, 8, "Unit Price", "1", 0, "R", false, 0, "")
    pdf.CellFormat(40, 8, "Line Total", "1", 1, "R", false, 0, "")
    pdf.SetFont("Arial", "", 12)
    for _, it := range inv.Items {
        line := it.Quantity * it.UnitPrice
        pdf.CellFormat(80, 8, it.Description, "1", 0, "L", false, 0, "")
        pdf.CellFormat(30, 8, fmt.Sprintf("%.2f", it.Quantity), "1", 0, "C", false, 0, "")
        pdf.CellFormat(40, 8, fmt.Sprintf("%.2f", it.UnitPrice), "1", 0, "R", false, 0, "")
        pdf.CellFormat(40, 8, fmt.Sprintf("%.2f", line), "1", 1, "R", false, 0, "")
    }
    pdf.Ln(4)
    pdf.CellFormat(150, 8, "Subtotal", "0", 0, "R", false, 0, "")
    pdf.CellFormat(40, 8, fmt.Sprintf("%.2f", inv.Subtotal), "0", 1, "R", false, 0, "")
    pdf.CellFormat(150, 8, "Tax", "0", 0, "R", false, 0, "")
    pdf.CellFormat(40, 8, fmt.Sprintf("%.2f", inv.TaxTotal), "0", 1, "R", false, 0, "")
    pdf.SetFont("Arial", "B", 12)
    pdf.CellFormat(150, 10, "Total", "0", 0, "R", false, 0, "")
    pdf.CellFormat(40, 10, fmt.Sprintf("%.2f", inv.Total), "0", 1, "R", false, 0, "")

    var buf bytes.Buffer
    if err := pdf.Output(&buf); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to generate pdf"})
        return
    }
    c.Header("Content-Disposition", "attachment; filename=invoice-"+inv.InvoiceID+".pdf")
    c.Data(http.StatusOK, "application/pdf", buf.Bytes())
}

// Share over WhatsApp (stub). Accepts JSON: { "phone": "+911234567890" }
// In production, integrate with WhatsApp Cloud API or Twilio WhatsApp API.
type shareRequest struct {
    Phone string `json:"phone" binding:"required"`
}

func (h *InvoiceHandler) ShareWhatsApp(c *gin.Context) {
    var req shareRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    // For now, just pretend we sent the PDF. You can integrate an API here.
    c.JSON(http.StatusOK, gin.H{"status": "queued", "message": "WhatsApp send stub", "phone": req.Phone})
}


