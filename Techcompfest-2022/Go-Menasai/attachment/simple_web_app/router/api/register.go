package api

import (
	"net/http"

	"github.com/dimasma0305/simple_web_app/helpers"
	"github.com/dimasma0305/simple_web_app/model"
	"github.com/gin-contrib/sessions"
	"github.com/gin-gonic/gin"
)

func Register(c *gin.Context) {
	var u model.User
	session := sessions.Default(c)

	if err := c.ShouldBind(&u); err != nil {
		c.AbortWithStatusJSON(http.StatusBadRequest, gin.H{
			"error": err.Error(),
		})
		return
	}

	md5pass, _ := helpers.HashPassword(u.Password)

	newUser := model.User{
		Username: u.Username,
		Hash:     md5pass,
	}
	db, err := model.Database()

	if err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, gin.H{
			"error": err.Error(),
		})
		return
	}

	if err := db.Create(&newUser).Error; err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, gin.H{
			"error": err.Error(),
		})
		return
	}

	session.Set("ID", newUser.ID)
	session.Save()

	c.JSON(http.StatusOK, newUser)

}
