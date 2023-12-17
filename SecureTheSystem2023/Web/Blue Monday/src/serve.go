package main

import (
	"github.com/gin-gonic/gin"
)

func serve(file string) func(ctx *gin.Context) {
	return func(ctx *gin.Context) {
		fileValue, err := view.ReadFile("view/" + file)
		if err != nil {
			ctx.JSONP(200, map[string]interface{}{"message": err.Error()})
			return
		}
		ctx.String(200, string(fileValue))
	}
}

func serveXHTML(file string) func(ctx *gin.Context) {
	return func(ctx *gin.Context) {
		ctx.Header("content-type", "application/xhtml+xml")
		ctx.Header("content-security-policy", "script-src 'self' https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js")
		serve(file)(ctx)
	}
}
