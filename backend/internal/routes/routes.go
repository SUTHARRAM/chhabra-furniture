package routes

import (
	"github.com/gin-gonic/gin"
	"github.com/SUTHARRAM/chhabra-furniture/internal/config"
	"github.com/SUTHARRAM/chhabra-furniture/internal/handlers"
	"github.com/SUTHARRAM/chhabra-furniture/internal/middleware"
	"github.com/SUTHARRAM/chhabra-furniture/internal/repository"
	"github.com/SUTHARRAM/chhabra-furniture/internal/services"
	"go.mongodb.org/mongo-driver/mongo"
)

func SetupRouter(cfg config.Config, client *mongo.Client) *gin.Engine {
	r := gin.Default()
	r.SetTrustedProxies(nil)

	ur := repository.NewUserRepo(client, cfg.MongoDB)
	br := repository.NewBillRepo(client, cfg.MongoDB)
	st, _ := services.NewStorage(cfg.MinIOEndpoint, cfg.MinIOAccessKey, cfg.MinIOSecretKey, cfg.MinIOUseSSL, cfg.MinIOBucket)

	authH := handlers.NewAuthHandler(cfg, ur)
	billH := handlers.NewBillHandler(cfg, br, st)

	api := r.Group("/api/v1")

	api.POST("/auth/login", authH.Login)

	authed := api.Group("/")
	authed.Use(middleware.Auth(cfg.JWTSecret)) // any role
	{
		authed.POST("/bills", billH.Create)
		authed.GET("/bills", billH.List)
		authed.GET("/bills/:id", billH.Get)
		authed.POST("/bills/:id/pdf", billH.GenPDF)
		authed.GET("/bills/:id/share-links", billH.ShareLinks)
	}

	// Public share
	api.GET("/share/:slug", billH.PublicView)

	return r
}
