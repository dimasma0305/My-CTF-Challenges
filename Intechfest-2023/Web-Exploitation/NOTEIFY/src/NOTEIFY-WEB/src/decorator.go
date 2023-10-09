package main

import (
	"encoding/base64"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
)

func bindUser(f func(c *gin.Context, user *User)) gin.HandlerFunc {
	return func(c *gin.Context) {
		var tuser struct {
			Username string
			Password string
		}
		if err := c.ShouldBindJSON(&tuser); err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, msgerror(err.Error()))
			return
		}
		user := &User{
			Username: tuser.Username,
			Password: tuser.Password,
		}
		if err := validator.New().Struct(user); err != nil {
			c.AbortWithStatusJSON(http.StatusBadRequest, msgerror("The username or password must be between 8 and 20 characters in length"))
			return
		}
		f(c, user)
	}
}

func requireAuth(f func(c *gin.Context, user *User)) gin.HandlerFunc {
	return func(c *gin.Context) {
		authHeader := c.Request.Header.Get("Authorization")
		if authHeader == "" {
			// Return an error response if the header is missing
			c.AbortWithStatusJSON(http.StatusUnauthorized, msgerror("Missing Authorization header"))
			return
		}

		// Parse the Authorization header value
		parts := strings.SplitN(authHeader, " ", 2)
		if len(parts) != 2 || strings.ToLower(parts[0]) != "bearer" {
			// Return an error response if the header is not in the expected format
			c.AbortWithStatusJSON(http.StatusUnauthorized, msgerror("Invalid Authorization header"))
			return
		}

		base64creds, err := base64.StdEncoding.DecodeString(parts[1])
		if err != nil {
			c.AbortWithStatusJSON(http.StatusInternalServerError, msgerror(err.Error()))
			return
		}
		creds := strings.SplitN(string(base64creds), ":", 2)
		username := strings.TrimSpace(string(creds[0]))
		password := strings.TrimSpace(string(creds[1]))
		var user *User
		if err := db.Where(&User{
			Username: username,
			Password: password,
		}).First(&user).Error; err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, msgerror("username or password is incorrect"))
			return
		}
		f(c, user)
	}
}
