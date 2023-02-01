package home

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// Login front end
func Login(c *gin.Context){
	c.HTML(http.StatusOK, "login.html", nil)
}