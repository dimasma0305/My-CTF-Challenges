package main

import (
	"crypto/rand"
	"encoding/hex"
	"os"

	"github.com/dimasma0305/simple_web_app/helpers"
	"github.com/dimasma0305/simple_web_app/model"
	"github.com/dimasma0305/simple_web_app/router"
	"github.com/gin-contrib/sessions"
	"github.com/gin-contrib/sessions/cookie"
	"github.com/gin-gonic/gin"
	"github.com/labstack/gommon/log"
)

type Setup struct{ *gin.Engine }

func (e Setup) setup() {
	e.LoadHTMLGlob("templates/*.html")
	e.SetSession()
	e.SetDatabases()
	e.SetRouter()
}

func (e Setup) SetRouter() {
	router.New(e.Engine).Start()
}

func (e Setup) SetSession() {
	sessionKey := os.Getenv("SESSION_KEY")
	if sessionKey == "" {
		key := make([]byte, 16)
		rand.Read(key)
		sessionKey := key
		log.Infof("Session Key: %s", sessionKey)
	}
	store := cookie.NewStore([]byte(sessionKey))
	e.Use(sessions.Sessions("session", store))
}

func (e Setup) SetDatabases() {
	password := genPassword()
	hash, _ := helpers.HashPassword(password)
	user := model.User{
		Username: "dimas",
		Password: password,
		Hash:     hash,
		IsAdmin:  true,
	}
	db, err := model.Database()
	if err != nil {
		log.Error(err)
		return
	}
	if err := db.Create(&user).Error; err != nil {
		log.Error(err)
		return
	}

}

func genPassword() string {
	passbyte := make([]byte, 16)
	rand.Read(passbyte)
	password := hex.EncodeToString(passbyte)
	log.Infof("password: %s", password)
	return password
}
