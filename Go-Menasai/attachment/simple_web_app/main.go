package main

import (
	"github.com/gin-gonic/gin"
)

func main() {
	println("hello")
	r := gin.Default()
	Setup{r}.setup()
	r.Run()
}
