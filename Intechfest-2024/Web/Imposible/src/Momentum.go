package main

type Handler interface{}

type Momentum struct {
	mws []Middleware
}
