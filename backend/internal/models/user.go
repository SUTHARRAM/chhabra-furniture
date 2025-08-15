package models

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
	"golang.org/x/crypto/bcrypt"
)

type User struct {
	ID           primitive.ObjectID `bson:"_id,omitempty" json:"id"`
	Name         string             `bson:"name" json:"name"`
	Email        string             `bson:"email" json:"email"`
	PasswordHash string             `bson:"password_hash" json:"-"`
	Role         string             `bson:"role" json:"role"`
	CreatedAt    time.Time          `bson:"created_at" json:"created_at"`
	UpdatedAt    time.Time          `bson:"updated_at" json:"updated_at"`
}

func NewUser(email, name, password, role string) User {
	hash, _ := bcrypt.GenerateFromPassword([]byte(password), 12)
	now := time.Now()
	return User{
		Name: name, Email: email, PasswordHash: string(hash),
		Role: role, CreatedAt: now, UpdatedAt: now,
	}
}

func (u *User) CheckPassword(pw string) bool {
	return bcrypt.CompareHashAndPassword([]byte(u.PasswordHash), []byte(pw)) == nil
}
