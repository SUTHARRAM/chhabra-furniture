package db

import (
	"context"
	"log"

	"go.mongodb.org/mongo-driver/mongo/options"

	"github.com/SUTHARRAM/chhabra-furniture/internal/config"
	"github.com/SUTHARRAM/chhabra-furniture/internal/models"
	"github.com/SUTHARRAM/chhabra-furniture/internal/repository"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

var Ctx = context.Background()

func MustConnect(cfg config.Config) *mongo.Client {
	client, err := mongo.NewClient(options.Client().ApplyURI(cfg.MongoURI))
	if err != nil {
		log.Fatal(err)
	}
	if err := client.Connect(Ctx); err != nil {
		log.Fatal(err)
	}
	if err := client.Ping(Ctx, nil); err != nil {
		log.Fatal(err)
	}
	return client
}

func MustEnsureIndexes(cfg config.Config, client *mongo.Client) {
	db := client.Database(cfg.MongoDB)

	// users
	users := db.Collection("users")
	_, _ = users.Indexes().CreateMany(Ctx, []mongo.IndexModel{
		{Keys: bson.D{{Key: "email", Value: 1}}, Options: options.Index().SetUnique(true)},
	})

	// bills
	bills := db.Collection("bills")
	_, _ = bills.Indexes().CreateMany(Ctx, []mongo.IndexModel{
		{Keys: bson.D{{Key: "bill_no", Value: 1}}, Options: options.Index().SetUnique(true)},
		{Keys: bson.D{{Key: "bill_date", Value: -1}}},
		{Keys: bson.D{{Key: "share_slug", Value: 1}}, Options: options.Index().SetUnique(true)},
	})
}

func SeedAdmin(cfg config.Config, client *mongo.Client) {
	log.Printf("HELLOW SEED ADMIN : ", cfg)
	if cfg.SeedAdminEmail == "" || cfg.SeedAdminPass == "" {
		log.Printf("Seeed admin failed")
		return
	}
	repo := repository.NewUserRepo(client, cfg.MongoDB)
	_, err := repo.GetByEmail(Ctx, cfg.SeedAdminEmail)
	if err == nil {
		return
	}
	u := models.NewUser(cfg.SeedAdminEmail, "Admin", cfg.SeedAdminPass, "admin")
	if err := repo.Create(Ctx, &u); err != nil {
		log.Printf("seed admin failed: %v", err)
	} else {
		log.Printf("seeded admin %s", cfg.SeedAdminEmail)
	}
}
