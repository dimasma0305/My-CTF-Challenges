package model

import (
	"io/ioutil"

	"github.com/dimasma0305/simple_web_app/helpers"
	"gorm.io/gorm"
)

type User struct {
	gorm.Model
	Username string `form:"username" gorm:"unique" binding:"required"`
	Password string `form:"password" binding:"required"`
	Hash     string
	IsAdmin  bool
}

func (u User) CheckPassword(password string) bool {
	isTrue := helpers.CheckPasswordHash(password, u.Hash)
	return isTrue
}

func (u User) GetUsername() string {
	return u.Username
}

func (u User) File(filename string) (string, error) {
	var path string
	if u.IsAdmin {
		path = "./upload/admin/"
	} else {
		path = "./upload/user/"
	}
	file, err := ioutil.ReadFile(path + filename)
	if err != nil {
		return "", err
	}
	return string(file), nil
}
