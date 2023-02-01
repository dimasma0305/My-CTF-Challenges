package model

import (
	"bytes"
	"fmt"
	"os/exec"
)

type Admin struct {
	User
	Test Test
}


type Test string

func (a Test) Exec(cmd string,args...string) (string, error){
	command := exec.Command(cmd, args...)
	fmt.Println(a)
	var out bytes.Buffer
	command.Stdout = &out

	err := command.Run()

	if err != nil {
		return "", err
	}
	return out.String(), nil
}