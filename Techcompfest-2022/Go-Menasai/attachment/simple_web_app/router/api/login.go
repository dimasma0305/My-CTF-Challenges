package api

import (
	"net/http"

	"github.com/dimasma0305/simple_web_app/model"
	"github.com/gin-contrib/sessions"
	"github.com/gin-gonic/gin"
)

func Login(c *gin.Context) {
	var user model.User
	session := sessions.Default(c)
	db, _ := model.Database()

	if err := c.ShouldBind(&user); err != nil {
		c.AbortWithStatusJSON(http.StatusBadRequest, gin.H{
			"error": err.Error(),
		})
		return
	}

	password := user.Password
	if err := db.Where("Username = ?", user.Username).First(&user).Error; err != nil {
		c.AbortWithStatusJSON(http.StatusNotFound, gin.H{
			"error": "username not found",
		})
		return
	}
	
	isPassword := user.CheckPassword(password)
	if !isPassword {
		c.AbortWithStatusJSON(http.StatusNotFound, gin.H{
			"error": "username and password didn't match",
		})
		return
	}

	session.Set("ID", user.ID)
	session.Save()

	c.JSON(http.StatusAccepted, gin.H{
		"message": "success",
	})
}
