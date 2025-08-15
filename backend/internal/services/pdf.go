package services

import (
	"bytes"
	"fmt"

	"github.com/jung-kurt/gofpdf"
	"github.com/SUTHARRAM/chhabra-furniture/internal/models"
)

func GenerateInvoicePDF(inv models.Bill, fontPath, logoPath string) (*bytes.Buffer, error) {
	pdf := gofpdf.New("P", "mm", "A4", "")
	pdf.AddUTF8Font("NotoSans", "", fontPath)
	pdf.SetFont("NotoSans", "", 12)
	pdf.AddPage()

	// Vishwakarma image (top-right corner)
	pdf.ImageOptions(logoPath, 180, 5, 20, 0, false, gofpdf.ImageOptions{ImageType: "PNG"}, 0, "")

	// Header
	pdf.Cell(40, 10, get(inv.Language, "Invoice", "बिल"))
	pdf.Ln(12)

	// From / To
	pdf.SetFont("NotoSans", "", 10)
	pdf.Cell(95, 6, get(inv.Language, "From", "प्रेषक")+": "+inv.From.Name)
	pdf.Cell(95, 6, get(inv.Language, "To", "प्राप्तकर्ता")+": "+inv.To.Name)
	pdf.Ln(6)
	pdf.Cell(95, 6, inv.From.Address)
	pdf.Cell(95, 6, inv.To.Address)
	pdf.Ln(10)

	// Items table
	pdf.SetFont("NotoSans", "", 10)
	pdf.CellFormat(110, 7, get(inv.Language, "Description", "उत्पाद विवरण"), "1", 0, "", false, 0, "")
	pdf.CellFormat(20, 7, get(inv.Language, "Rate", "दर"), "1", 0, "", false, 0, "")
	pdf.CellFormat(20, 7, get(inv.Language, "Qty", "मात्रा"), "1", 0, "", false, 0, "")
	pdf.CellFormat(40, 7, get(inv.Language, "Price", "कीमत"), "1", 0, "", false, 0, "")
	pdf.Ln(-1)
	for _, it := range inv.Items {
		pdf.CellFormat(110, 7, it.Description, "1", 0, "", false, 0, "")
		pdf.CellFormat(20, 7, money(it.Rate), "1", 0, "", false, 0, "")
		pdf.CellFormat(20, 7, fmt.Sprintf("%.2f", it.Quantity), "1", 0, "", false, 0, "")
		pdf.CellFormat(40, 7, money(it.Price), "1", 0, "", false, 0, "")
		pdf.Ln(-1)
	}
	pdf.Ln(2)
	pdf.Cell(150, 7, get(inv.Language, "Subtotal", "उप-योग"))
	pdf.Cell(40, 7, money(inv.Subtotal))
	pdf.Ln(7)
	pdf.Cell(150, 7, inv.Tax.Label)
	pdf.Cell(40, 7, money(inv.Tax.Amount))
	pdf.Ln(7)
	pdf.Cell(150, 7, get(inv.Language, "Discount", "छूट"))
	pdf.Cell(40, 7, money(inv.Discount))
	pdf.Ln(7)
	pdf.Cell(150, 7, get(inv.Language, "Total", "कुल"))
	pdf.Cell(40, 7, money(inv.Total))
	pdf.Ln(10)
	pdf.MultiCell(190, 6, get(inv.Language, "Thank you for your business!", "धन्यवाद!"), "", "", false)

	var buf bytes.Buffer
	if err := pdf.Output(&buf); err != nil {
		return nil, err
	}
	return &buf, nil
}

func money(f float64) string { return fmt.Sprintf("₹%.2f", f) }

func get(lang, en, hi string) string {
	if lang == "hi" { return hi }
	return en
}
