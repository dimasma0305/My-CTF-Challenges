package main

import (
	"log"
	"os"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

type User struct {
	ID       uint   `gorm:"primarykey"`
	Username string `gorm:"not null;unique" validate:"min=5,max=20"`
	Password string `gorm:"not null" validate:"min=5,max=64"`
	Notes    []Note `gorm:"foreignKey:OwnerID"`
}

type Note struct {
	ID      string `gorm:"primarykey" validate:"uuid"`
	Title   string `gorm:"not null" validate:"min=1"`
	Content string `gorm:"not null"`
	OwnerID uint   `gorm:"not null"`
}

var (
	Username = os.Getenv("TARGET_USERNAME")
	Password = os.Getenv("TARGET_PASSWORD")
)

func initDb() {
	db, err := gorm.Open(sqlite.Open("./database.db"), &gorm.Config{})
	if err != nil {
		log.Fatal(err.Error())
	}
	if err = db.AutoMigrate(&User{}, &Note{}); err != nil {
		log.Fatal(err)
	}
	log.Println("Username:", Username)
	log.Println("Password:", Password)
	if err := db.Create(&User{Username: Username, Password: Password}).Error; err != nil {
		log.Println(err)
	}
}

func database() *gorm.DB {
	db, err := gorm.Open(sqlite.Open("./database.db"), &gorm.Config{})
	if err != nil {
		log.Fatal(err.Error())
	}
	return db

}
