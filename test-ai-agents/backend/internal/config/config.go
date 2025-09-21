package config

import (
	"os"
)

type Config struct {
	Env           string
	Port          string
	MongoURI      string
	MongoDatabase string
	JWTSecret     string
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func Load() Config {
	return Config{
		Env:           getEnv("APP_ENV", "development"),
		Port:          getEnv("PORT", "8080"),
		MongoURI:      getEnv("MONGO_URI", "mongodb://mongo:27017"),
		MongoDatabase: getEnv("MONGO_DB", "invoice_app"),
		JWTSecret:     getEnv("JWT_SECRET", "change-me-in-prod"),
	}
}


