package router

import (
	"github.com/dimasma0305/simple_web_app/router/api"
	"github.com/dimasma0305/simple_web_app/router/home"
	"github.com/gin-gonic/gin"
)

type Router struct {
	*gin.Engine
}

// Alocate new Router struct
func New(c *gin.Engine) *Router {
	return &Router{c}
}

func (r Router) api() {
	g := r.Group("/api")
	g.POST("/login", api.Login)
	g.POST("/register", api.Register)
	g.POST("/logout", api.Logout)
}

func (r Router) home(){
	r.GET("/", home.Home)
	r.GET("/login", home.Login)
	r.GET("/register", home.Register)
	
}

// start of the router 
func (r Router) Start(){
	r.api()
	r.home()
}

