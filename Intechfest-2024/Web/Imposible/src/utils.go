package main

import (
	"net/http"
)

func getMWFromHandler(handler Handler) Middleware {
	if mw, ok := handler.(func(http.Handler) http.Handler); ok {
		return mw
	}
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			handler.(http.Handler).ServeHTTP(w, r)
			next.ServeHTTP(w, r)
		})
	}
}
