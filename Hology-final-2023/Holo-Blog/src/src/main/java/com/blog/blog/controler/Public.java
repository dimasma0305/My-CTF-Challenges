package com.blog.blog.controler;

import javax.servlet.http.HttpSession;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class Public {
    @GetMapping("/")
    String index(HttpSession session) throws Exception {
        String lang = (String) session.getAttribute("lang");
        return String.format("lang/%s/index", lang);
    }
}
