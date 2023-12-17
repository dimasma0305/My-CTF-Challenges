package com.example.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class Pages {
    @GetMapping("/")
    public String main() {
        return "main";
    }

    @GetMapping("/login")
    public String login() {
        return "login";
    }

    @GetMapping("/blog")
    public String blog(){
        return "blog";
    }
}
