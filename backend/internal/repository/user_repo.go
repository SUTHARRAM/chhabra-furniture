package repository

import (
	"context"

	"github.com/SUTHARRAM/chhabra-furniture/internal/models"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

type UserRepo struct {
	col *mongo.Collection
}

func NewUserRepo(client *mongo.Client, dbName string) *UserRepo {
	return &UserRepo{col: client.Database(dbName).Collection("users")}
}

func (r *UserRepo) Create(ctx context.Context, u *models.User) error {
	_, err := r.col.InsertOne(ctx, u)
	return err
}

func (r *UserRepo) GetByEmail(ctx context.Context, email string) (*models.User, error) {
	var u models.User
	err := r.col.FindOne(ctx, bson.M{"email": email}).Decode(&u)
	return &u, err
}
