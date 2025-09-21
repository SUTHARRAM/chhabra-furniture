package router

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/yourorg/invoice-app/backend/internal/config"
	"github.com/yourorg/invoice-app/backend/internal/handlers"
	"github.com/yourorg/invoice-app/backend/internal/middleware"
)

func RegisterRoutes(r *gin.Engine, cfg config.Config) {
	// Health
	r.GET("/health", func(c *gin.Context) { c.JSON(http.StatusOK, gin.H{"status": "ok"}) })

	// Auth endpoints
	ah := handlers.NewAuthHandler(cfg)
	auth := r.Group("/api/auth")
	{
		auth.POST("/login", ah.Login)
		auth.POST("/register", ah.Register)
	}

	// Protected invoice routes (CRUD, search, pdf, share)
	api := r.Group("/api")
	api.Use(middleware.AuthRequired(cfg.JWTSecret))
	{
		ih := handlers.NewInvoiceHandler()
		api.GET("/invoices", ih.List)
		api.POST("/invoices", ih.Create)
		api.GET("/invoices/:id", ih.Get)
		api.PUT("/invoices/:id", ih.Update)
		api.DELETE("/invoices/:id", ih.Delete)
		api.GET("/invoices/:id/pdf", ih.ExportPDF)
		api.POST("/invoices/:id/share/whatsapp", ih.ShareWhatsApp)
	}
}