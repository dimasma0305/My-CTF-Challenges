package home

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// register front end
func Register(c *gin.Context){
	c.HTML(http.StatusOK, "register.html", nil)
}