package config

import (
	"fmt"
	"os"
)

type Config struct {
	Port           string
	MongoURI       string
	MongoDB        string
	JWTSecret      string
	JWTExpireHours int
	MinIOEndpoint  string
	MinIOAccessKey string
	MinIOSecretKey string
	MinIOBucket    string
	MinIOUseSSL    bool
	SeedAdminEmail string
	SeedAdminPass  string
}

func Load() Config {
	return Config{
		Port:           get("PORT", "8080"),
		MongoURI:       get("MONGO_URI", "mongodb://localhost:27017"),
		MongoDB:        get("MONGO_DB", "chhabra"),
		JWTSecret:      get("JWT_SECRET", "change_me"),
		JWTExpireHours: atoi(get("JWT_EXPIRE_HOURS", "12")),
		MinIOEndpoint:  get("MINIO_ENDPOINT", "localhost:9000"),
		MinIOAccessKey: get("MINIO_ACCESS_KEY", ""),
		MinIOSecretKey: get("MINIO_SECRET_KEY", ""),
		MinIOBucket:    get("MINIO_BUCKET", "invoices"),
		MinIOUseSSL:    get("MINIO_USE_SSL", "false") == "true",
		SeedAdminEmail: get("SEED_ADMIN_EMAIL", ""),
		SeedAdminPass:  get("SEED_ADMIN_PASSWORD", ""),
	}
}

func get(k, d string) string {
	if v := os.Getenv(k); v != "" {
		return v
	}
	return d
}

func atoi(s string) int {
	var n int
	_, _ = fmt.Sscanf(s, "%d", &n)
	return n
}
