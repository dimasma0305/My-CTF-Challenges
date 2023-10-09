package api

import (
	"net/http"

	"github.com/gin-contrib/sessions"
	"github.com/gin-gonic/gin"
)

func Logout(c *gin.Context){
	session := sessions.Default(c)
	session.Clear()
	session.Save()
	c.JSON(http.StatusAccepted, gin.H{
		"message":"success",
	})
}