package main

import (
	"log"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/yourorg/invoice-app/backend/internal/config"
	"github.com/yourorg/invoice-app/backend/internal/db"
	"github.com/yourorg/invoice-app/backend/internal/router"
)

func main() {
	// Load config from environment
	cfg := config.Load()

	// Initialize database connection
	if err := db.Connect(cfg.MongoURI, cfg.MongoDatabase); err != nil {
		log.Fatalf("failed to connect to MongoDB: %v", err)
	}

	// Set Gin mode
	if cfg.Env == "production" {
		gin.SetMode(gin.ReleaseMode)
	}

	r := gin.Default()
	router.RegisterRoutes(r, cfg)

	addr := ":" + cfg.Port
	if p := os.Getenv("PORT"); p != "" {
		addr = ":" + p
	}
	log.Printf("server listening on %s", addr)
	if err := r.Run(addr); err != nil {
		log.Fatalf("server error: %v", err)
	}
}


