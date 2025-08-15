package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/SUTHARRAM/chhabra-furniture/internal/config"
	"github.com/SUTHARRAM/chhabra-furniture/internal/repository"
	"github.com/SUTHARRAM/chhabra-furniture/internal/services"
)

type AuthHandler struct {
	cfg config.Config
	ur  *repository.UserRepo
}

func NewAuthHandler(cfg config.Config, ur *repository.UserRepo) *AuthHandler { return &AuthHandler{cfg, ur} }

type loginReq struct {
	Email string `json:"email" binding:"required,email"`
	Password string `json:"password" binding:"required"`
}

func (h *AuthHandler) Login(c *gin.Context) {
	var req loginReq
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()}); return
	}
	u, err := h.ur.GetByEmail(c, req.Email)
	if err != nil || !u.CheckPassword(req.Password) {
		c.JSON(http.StatusUnauthorized, gin.H{"error":"invalid credentials"}); return
	}
	token, _ := services.MakeJWT(h.cfg.JWTSecret, u.ID.Hex(), u.Role, h.cfg.JWTExpireHours)
	c.JSON(http.StatusOK, gin.H{"token": token, "user": gin.H{"id": u.ID.Hex(), "name": u.Name, "role": u.Role}})
}
