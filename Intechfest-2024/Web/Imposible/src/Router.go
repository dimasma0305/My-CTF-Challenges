package main

import (
	"net/http"
)

type Router struct {
	routes map[string]http.HandlerFunc
	m      *Momentum
}

func MakeRouter() *Router {
	return &Router{
		routes: map[string]http.HandlerFunc{},
		m:      &Momentum{},
	}
}

func (rtr *Router) UseMiddleware(mw Middleware) {
	rtr.m.mws = append(rtr.m.mws, mw)
}

func (rtr *Router) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	handler, exists := rtr.routes[r.URL.Path]
	if exists {
		handler.ServeHTTP(w, r)
		return
	}
	http.NotFound(w, r)
}

func (rtr *Router) Handle(pattern string, handlers []Handler) {
	rtr.routes[pattern] = func(resp http.ResponseWriter, req *http.Request) {
		mws := rtr.m.mws

		for _, h := range handlers {
			mws = append(mws, getMWFromHandler(h))
		}

		h := http.Handler(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {}))
		for i := len(mws) - 1; i >= 0; i-- {
			h = mws[i](h)
		}
		h.ServeHTTP(resp, req)
	}
}

func (rtr *Router) Get(pattern string, h ...Handler)  { rtr.Handle(pattern, h) }
func (rtr *Router) Post(pattern string, h ...Handler) { rtr.Handle(pattern, h) }
