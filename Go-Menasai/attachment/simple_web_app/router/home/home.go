package home

import (
	"bytes"
	"net/http"
	"text/template"

	"github.com/dimasma0305/simple_web_app/model"
	"github.com/gin-contrib/sessions"
	"github.com/gin-gonic/gin"
)

type Query struct {
	Test string `json:"test"`
}

func user_home(parse *template.Template, c *gin.Context, user model.User) {
	var new_buf bytes.Buffer
	parse.Execute(&new_buf, user)
	c.HTML(http.StatusOK, "home.html", gin.H{
		"template": new_buf.String(),
	})
}

func admin_home(parse *template.Template, c *gin.Context, user model.User) {
	admin := model.Admin{
		User: user,
	}
	var query Query
	var nameTemplate bytes.Buffer
	var testTemplate bytes.Buffer

	/**
	* For testing purpose, please remove in production
	**/
	c.Bind(&query)
	if query.Test != "" {
		testParse, err := template.New("test template").Parse(
			`testing `+query.Test,
		)
		if err != nil {
			c.AbortWithError(http.StatusInternalServerError, err)
			return
		}
		testParse.Execute(&testTemplate, admin)
	}
	parse.Execute(&nameTemplate, admin)
	c.HTML(http.StatusOK, "home.html", gin.H{
		"template": nameTemplate.String(),
		"test": testTemplate.String(),
	})
}

// Home page /
func Home(c *gin.Context) {
	session := sessions.Default(c)

	var user model.User
	var id = session.Get("ID")
	if id == nil {
		c.Redirect(http.StatusTemporaryRedirect, "/register")
		return
	}

	db, err := model.Database()
	if err != nil {
		c.AbortWithError(http.StatusInternalServerError, err)
		return
	}

	if err := db.Where("ID = ?", session.Get("ID")).First(&user).Error; err != nil {
		c.Redirect(http.StatusTemporaryRedirect, "/register")
		return
	}

	name := user.Username
	if name == "" {
		c.Redirect(http.StatusTemporaryRedirect, "/register")
		return
	}
	parse, err := template.New("my template").Parse(
		`Welcome {{if .IsAdmin}} admin {{else}} user {{end}} ` + user.Username + `!`,
	)
	if err != nil {
		c.AbortWithError(http.StatusInternalServerError, err)
		return
	}

	if user.IsAdmin {
		admin_home(parse, c, user)
	} else {
		user_home(parse, c, user)
	}
}
