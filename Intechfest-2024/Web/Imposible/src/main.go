package main

import (
	"net/http"
)

func main() {
	r := MakeRouter()

	r.UseMiddleware(logMiddleware)
	r.UseMiddleware(antiXSS)
	r.UseMiddleware(cspProtection)

	r.Get("/", http.HandlerFunc(indexView))

	r.Get("/flag", adminOnly, http.HandlerFunc(flagHandler))

	http.ListenAndServe(":8080", r)
}
