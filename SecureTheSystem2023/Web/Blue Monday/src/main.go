package main

import (
	"embed"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/microcosm-cc/bluemonday"
	"log"
	"net/http"
	"strings"
)

var (
	//go:embed view/*
	view embed.FS
	//go:embed public/*
	public embed.FS
	notes  = make(map[string]string)
)

func main() {
	r := gin.Default()
	r.GET("/", serveXHTML("index.xhtml"))
	r.GET("/note", serveXHTML("note.xhtml"))
	r.GET("/note/:id", serveXHTML("note_id.xhtml"))
	r.StaticFS("/public", http.FS(newPublicFS(public)))
	r.POST("/api/v1/note", func(context *gin.Context) {
		sanitizer := bluemonday.UGCPolicy()
		sanitizer.AllowElements(CommonElements...)
		sanitizer.AllowUnsafe(true)
		uuidString := uuid.New().String()
		value, _ := context.GetPostForm("value")
		notes[uuidString] = sanitizer.Sanitize(value)
		context.Redirect(302, "/note/"+uuidString)
	})
	r.GET("/static/:file", func(context *gin.Context) {
		file := context.Param("file")
		if strings.HasSuffix(file, ".xhtml") {
			serveXHTML(file)(context)
		} else {
			serve(file)(context)
		}
	})
	r.GET("/api/v1/note/:id", func(context *gin.Context) {
		uuidString := context.Param("id")
		context.String(200, notes[uuidString])
	})
	if err := r.Run("0.0.0.0:8080"); err != nil {
		log.Fatal(err)
	}
}
