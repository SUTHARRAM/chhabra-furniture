package models

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type Party struct {
	Name    string `bson:"name" json:"name"`
	Address string `bson:"address" json:"address"`
	Phone   string `bson:"phone" json:"phone"`
	GSTIN   string `bson:"gstin" json:"gstin"`
}

type Item struct {
	Description string  `bson:"description" json:"description"`
	Rate        float64 `bson:"rate" json:"rate"`
	Quantity    float64 `bson:"quantity" json:"quantity"`
	Unit        string  `bson:"unit" json:"unit"`
	Price       float64 `bson:"price" json:"price"`
}

type Tax struct {
	Label  string  `bson:"label" json:"label"`
	Amount float64 `bson:"amount" json:"amount"`
}

type Bill struct {
	ID        primitive.ObjectID `bson:"_id,omitempty" json:"id"`
	BillNo    string             `bson:"bill_no" json:"bill_no"`
	BillDate  time.Time          `bson:"bill_date" json:"bill_date"`
	From      Party              `bson:"from" json:"from"`
	To        Party              `bson:"to" json:"to"`
	Items     []Item             `bson:"items" json:"items"`
	Currency  string             `bson:"currency" json:"currency"`
	Subtotal  float64            `bson:"subtotal" json:"subtotal"`
	Discount  float64            `bson:"discount" json:"discount"`
	Tax       Tax                `bson:"tax" json:"tax"`
	Total     float64            `bson:"total" json:"total"`
	Notes     string             `bson:"notes" json:"notes"`
	Language  string             `bson:"language" json:"language"` // "en" or "hi"
	PDF       struct {
		S3Key           string `bson:"s3_key" json:"s3_key"`
		SignedURLExpiry int    `bson:"signed_url_expiry" json:"signed_url_expiry"`
	} `bson:"pdf" json:"pdf"`
	CreatedBy primitive.ObjectID `bson:"created_by" json:"created_by"`
	Status    string             `bson:"status" json:"status"` // draft/finalized
	ShareSlug string             `bson:"share_slug" json:"share_slug"`
	Deleted   bool               `bson:"deleted" json:"deleted"`
	CreatedAt time.Time          `bson:"created_at" json:"created_at"`
	UpdatedAt time.Time          `bson:"updated_at" json:"updated_at"`
}
