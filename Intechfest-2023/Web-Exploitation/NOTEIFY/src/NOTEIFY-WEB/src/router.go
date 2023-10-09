package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
	"github.com/google/uuid"
)

var (
	db = database()
)

func routes() {
	app := gin.Default()
	app.GET("/", home)
	api := app.Group("/api")
	api.POST("/login", bindUser(login))
	api.POST("/register", bindUser(register))
	api.POST("/addnote", requireAuth(addNote))
	api.GET("/getnote/:id", requireAuth(getNote))
	api.GET("/getnotes", requireAuth(getNotes))
	api.GET("/healthcheck", healthcheck)
	app.Run()
}
func home(c *gin.Context) {
	c.File("index.html")
}

// get all notes that associated with current user id
func getNotes(c *gin.Context, user *User) {
	var (
		notes []Note
	)
	if err := db.Where(&Note{OwnerID: user.ID}).Find(&notes).Error; err != nil {
		c.AbortWithStatusJSON(http.StatusNotFound, msgerror(err.Error()))
		return
	}
	c.JSONP(http.StatusOK, notes)
}

// healthcheck endpoint
func healthcheck(c *gin.Context) {
	c.JSONP(http.StatusOK, message("success"))
}

// get note from database by note id
func getNote(c *gin.Context, user *User) {
	var (
		id   = c.Param("id")
		note Note
	)
	//
	if err := db.Where(&Note{ID: id}).First(&note).Error; err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, msgerror(err.Error()))
		return
	}
	if !(note.OwnerID == user.ID) {
		c.AbortWithStatusJSON(http.StatusForbidden, msgerror("permission error"))
		return
	}
	c.JSONP(http.StatusOK, note)
}

// add note from user json
func addNote(c *gin.Context, user *User) {
	var (
		note Note
		id   = uuid.New().String()
	)
	note.ID = id
	note.OwnerID = user.ID
	if err := c.ShouldBindJSON(&note); err != nil {
		c.AbortWithStatusJSON(http.StatusBadRequest, msgerror(err.Error()))
		return
	}
	if err := validator.New().Struct(&note); err != nil {
		c.AbortWithStatusJSON(http.StatusBadRequest, msgerror(err.Error()))
		return
	}
	if err := db.Create(note).Error; err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, msgerror(err.Error()))
		return
	}
	c.JSON(http.StatusOK, gin.H{"id": id})
}

// add username if username not in database
func login(c *gin.Context, user *User) {
	if err := db.Where(&user).First(&user).Error; err != nil {
		c.AbortWithStatusJSON(http.StatusUnauthorized, msgerror(err.Error()))
		return
	}
	c.JSON(200, message("success"))
}
func register(c *gin.Context, user *User) {
	if err := db.Create(&user).Error; err != nil {
		c.AbortWithStatusJSON(500, msgerror(err.Error()))
		return
	}
	c.JSON(200, message("success"))
}
func message(msg string) map[string]any {
	return gin.H{"message": msg}
}
func msgerror(msg string) map[string]any {
	return gin.H{"error": msg}
}
