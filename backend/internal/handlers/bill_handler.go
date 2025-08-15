package handlers

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/SUTHARRAM/chhabra-furniture/internal/config"
	"github.com/SUTHARRAM/chhabra-furniture/internal/models"
	"github.com/SUTHARRAM/chhabra-furniture/internal/repository"
	"github.com/SUTHARRAM/chhabra-furniture/internal/services"
	"github.com/SUTHARRAM/chhabra-furniture/internal/util"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

type BillHandler struct {
	cfg config.Config
	br  *repository.BillRepo
	st  *services.Storage
}

func NewBillHandler(cfg config.Config, br *repository.BillRepo, st *services.Storage) *BillHandler {
	return &BillHandler{cfg, br, st}
}

func (h *BillHandler) Create(c *gin.Context) {
	var b models.Bill
	if err := c.ShouldBindJSON(&b); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()}); return
	}

	// compute totals server-side
	var subtotal float64
	for i := range b.Items {
		b.Items[i].Price = b.Items[i].Rate * b.Items[i].Quantity
		subtotal += b.Items[i].Price
	}
	b.Subtotal = util.Round2(subtotal)
	total := subtotal - b.Discount + b.Tax.Amount
	b.Total = util.Round2(total)

	b.BillNo = util.NextBillNo()
	b.ShareSlug = util.RandomSlug(10)
	b.CreatedAt = time.Now()
	b.UpdatedAt = time.Now()

	uid := c.GetString("uid")
	if uid != "" { b.CreatedBy, _ = primitive.ObjectIDFromHex(uid) }

	if b.Language == "" { b.Language = "en" }
	if b.Currency == "" { b.Currency = "INR" }
	if b.Status == "" { b.Status = "finalized" }

	if err := h.br.Create(c, &b); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()}); return
	}
	c.JSON(http.StatusOK, b)
}

func (h *BillHandler) Get(c *gin.Context) {
	id, _ := primitive.ObjectIDFromHex(c.Param("id"))
	b, err := h.br.GetByID(c, id)
	if err != nil { c.JSON(http.StatusNotFound, gin.H{"error":"not found"}); return }
	c.JSON(http.StatusOK, b)
}

func (h *BillHandler) List(c *gin.Context) {
	page, limit := util.Atoi(c.Query("page"), 1), util.Atoi(c.Query("limit"), 20)
	var fromPtr, toPtr *time.Time
	if s := c.Query("date_from"); s != "" {
		if t, err := time.Parse(time.RFC3339, s); err == nil { fromPtr = &t }
	}
	if s := c.Query("date_to"); s != "" {
		if t, err := time.Parse(time.RFC3339, s); err == nil { toPtr = &t }
	}
	bills, total, err := h.br.Find(c, c.Query("q"), fromPtr, toPtr, c.Query("bill_no"), page, limit)
	if err != nil { c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()}); return }
	c.JSON(http.StatusOK, gin.H{"data": bills, "total": total, "page": page, "limit": limit})
}

func (h *BillHandler) GenPDF(c *gin.Context) {
	id, _ := primitive.ObjectIDFromHex(c.Param("id"))
	b, err := h.br.GetByID(c, id)
	if err != nil { c.JSON(http.StatusNotFound, gin.H{"error":"not found"}); return }

	buf, err := services.GenerateInvoicePDF(*b, "assets/fonts/NotoSans-Regular.ttf", "assets/images/vishwakarma.png")
	if err != nil { c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()}); return }

	key := "invoices/" + b.BillNo + ".pdf"
	if err := h.st.UploadPDF(c, key, buf); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()}); return
	}
	url, _ := h.st.Presign(c, key, time.Hour)

	_ = h.br.Update(c, b.ID, map[string]any{"pdf.s3_key": key})
	c.JSON(http.StatusOK, gin.H{"pdf_url": url, "s3_key": key})
}

func (h *BillHandler) PublicView(c *gin.Context) {
	slug := c.Param("slug")
	b, err := h.br.GetBySlug(c, slug)
	if err != nil { c.JSON(http.StatusNotFound, gin.H{"error":"not found"}); return }
	c.JSON(http.StatusOK, b)
}

func (h *BillHandler) ShareLinks(c *gin.Context) {
	id, _ := primitive.ObjectIDFromHex(c.Param("id"))
	b, err := h.br.GetByID(c, id)
	if err != nil { c.JSON(http.StatusNotFound, gin.H{"error":"not found"}); return }
	shareUrl := c.Request.Host + "/share/" + b.ShareSlug
	text := "Invoice " + b.BillNo + " - Total: ₹" + util.F2(b.Total) + " " + shareUrl
	c.JSON(http.StatusOK, gin.H{
		"public": "https://" + shareUrl,
		"whatsapp": "https://wa.me/?text=" + util.URLEncode(text),
		"facebook": "https://www.facebook.com/sharer/sharer.php?u=" + util.URLEncode("https://"+shareUrl),
	})
}
