package main

import (
	"log"

	"github.com/joho/godotenv"

	"github.com/SUTHARRAM/chhabra-furniture/internal/config"
	"github.com/SUTHARRAM/chhabra-furniture/internal/db"
	"github.com/SUTHARRAM/chhabra-furniture/internal/routes"
)

func main() {
	_ = godotenv.Load("/home/ram/mycode/chhabra-furniture/backend/.env") // in container .env is copied alongside
	cfg := config.Load()
	client := db.MustConnect(cfg)
	defer client.Disconnect(db.Ctx)

	db.MustEnsureIndexes(cfg, client)
	db.SeedAdmin(cfg, client)

	r := routes.SetupRouter(cfg, client)
	log.Printf("Server listening on :%s", cfg.Port)
	if err := r.Run(":" + cfg.Port); err != nil {
		log.Fatal(err)
	}
}
