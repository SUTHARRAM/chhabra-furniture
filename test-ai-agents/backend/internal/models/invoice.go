package models

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type InvoiceItem struct {
	Description string  `json:"description" bson:"description"`
	Quantity    float64 `json:"quantity" bson:"quantity"`
	UnitPrice   float64 `json:"unitPrice" bson:"unit_price"`
	TaxRate     float64 `json:"taxRate" bson:"tax_rate"`
}

type Invoice struct {
	ID          primitive.ObjectID `json:"id" bson:"_id,omitempty"`
	InvoiceID   string             `json:"invoiceId" bson:"invoice_id"`
	ClientName  string             `json:"clientName" bson:"client_name"`
	ClientEmail string             `json:"clientEmail" bson:"client_email"`
	ClientPhone string             `json:"clientPhone" bson:"client_phone"`
	Items       []InvoiceItem      `json:"items" bson:"items"`
	Subtotal    float64            `json:"subtotal" bson:"subtotal"`
	TaxTotal    float64            `json:"taxTotal" bson:"tax_total"`
	Total       float64            `json:"total" bson:"total"`
	Status      string             `json:"status" bson:"status"`
	CreatedAt   time.Time          `json:"createdAt" bson:"created_at"`
	UpdatedAt   time.Time          `json:"updatedAt" bson:"updated_at"`
}


