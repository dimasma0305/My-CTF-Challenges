package main

import (
	"fmt"
	_ "html/template"
	"net/http"
	"os"
)

func indexView(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("testing"))
}

func flagHandler(w http.ResponseWriter, r *http.Request) {
	flag := os.Getenv("FLAG")
	if flag == "" {
		flag = "INTECHFEST{test}"
	}
	fmt.Println("SOMEONE GOT THE FLAG!!!")
	w.Write([]byte(flag))
}
