package com.blog.blog.controler;

import java.sql.SQLException;

import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import javax.validation.Valid;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.servlet.view.RedirectView;

import com.blog.blog.db.User;
import com.blog.blog.validation.Lang;

import lombok.val;

@RestController
@RequestMapping("/api")
public class RestPublic {

    @PatchMapping("/lang")
    DefaultResponseFormat patchLang(@Valid @RequestBody(required = true) Lang data, HttpSession session)
            throws Exception {
        val defaultResponseFormat = new DefaultResponseFormat();
        val sessionId = session.getId();
        val user = new User();
        val role = user.getRole(sessionId);
        if ("guest".equals(role)) {
            throw new HttpClientErrorException(HttpStatus.UNAUTHORIZED, "Unauthorized");
        } else {
            session.setAttribute("lang", data.getLang());
            defaultResponseFormat.setMessage("ok");
        }
        return defaultResponseFormat;
    }

    @GetMapping("/refresh")
    RedirectView refresh(HttpSession session, HttpServletResponse response) throws SQLException {
        val redirectView = new RedirectView("/");
        val sessionId = session.getId();
        val user = new User();
        user.deleteUserByUserId(sessionId);
        response.setHeader("Set-Cookie", "JSESSIONID=null; Path=/; HttpOnly");
        return redirectView;
    }
}
