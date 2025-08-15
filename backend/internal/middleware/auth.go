package middleware

import (
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

func Auth(secret string, roles ...string) gin.HandlerFunc {
	allowed := map[string]bool{}
	for _, r := range roles { allowed[r] = true }

	return func(c *gin.Context) {
		h := c.GetHeader("Authorization")
		if !strings.HasPrefix(h, "Bearer ") {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error":"missing token"}); return
		}
		tokenStr := strings.TrimPrefix(h, "Bearer ")
		t, err := jwt.Parse(tokenStr, func(token *jwt.Token) (any, error) {
			return []byte(secret), nil
		})
		if err != nil || !t.Valid {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error":"invalid token"}); return
		}
		claims, ok := t.Claims.(jwt.MapClaims)
		if !ok { c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error":"bad claims"}); return }

		role := claims["role"].(string)
		if len(roles) > 0 && !allowed[role] {
			c.AbortWithStatusJSON(http.StatusForbidden, gin.H{"error":"forbidden"}); return
		}
		c.Set("uid", claims["uid"])
		c.Set("role", role)
		c.Next()
	}
}
