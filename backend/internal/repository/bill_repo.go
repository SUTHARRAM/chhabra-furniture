package repository

import (
	"context"
	"time"

	"github.com/SUTHARRAM/chhabra-furniture/internal/models"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type BillRepo struct {
	col *mongo.Collection
}

func NewBillRepo(client *mongo.Client, dbName string) *BillRepo {
	return &BillRepo{col: client.Database(dbName).Collection("bills")}
}

func (r *BillRepo) Create(ctx context.Context, b *models.Bill) error {
	_, err := r.col.InsertOne(ctx, b); return err
}

func (r *BillRepo) Update(ctx context.Context, id any, set bson.M) error {
	_, err := r.col.UpdateByID(ctx, id, bson.M{"$set": set}); return err
}

func (r *BillRepo) GetByID(ctx context.Context, id any) (*models.Bill, error) {
	var b models.Bill
	err := r.col.FindOne(ctx, bson.M{"_id": id}).Decode(&b)
	return &b, err
}

func (r *BillRepo) GetBySlug(ctx context.Context, slug string) (*models.Bill, error) {
	var b models.Bill
	err := r.col.FindOne(ctx, bson.M{"share_slug": slug}).Decode(&b)
	return &b, err
}

func (r *BillRepo) Find(ctx context.Context, q string, from, to *time.Time, billNo string, page, limit int) ([]models.Bill, int64, error) {
	filter := bson.M{"deleted": bson.M{"$ne": true}}
	if billNo != "" { filter["bill_no"] = billNo }
	if from != nil || to != nil {
		dr := bson.M{}
		if from != nil { dr["$gte"] = *from }
		if to != nil { dr["$lte"] = *to }
		filter["bill_date"] = dr
	}
	opts := options.Find().SetSort(bson.M{"bill_date": -1}).SetSkip(int64((page-1)*limit)).SetLimit(int64(limit))
	cur, err := r.col.Find(ctx, filter, opts)
	if err != nil { return nil, 0, err }
	defer cur.Close(ctx)
	var out []models.Bill
	for cur.Next(ctx) {
		var b models.Bill
		if err := cur.Decode(&b); err == nil { out = append(out, b) }
	}
	total, _ := r.col.CountDocuments(ctx, filter)
	return out, total, nil
}
