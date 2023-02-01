package main

import (
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	Setup{r}.setup()
	r.Run()
}
