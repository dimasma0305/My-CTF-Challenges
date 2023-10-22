package com.blog.blog.handler;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import org.springframework.http.HttpStatus;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.servlet.HandlerInterceptor;

import com.blog.blog.db.User;
import com.blog.blog.waf.WAF;
import lombok.val;

@Configuration
@Order(Integer.MIN_VALUE)
public class DefaultInteceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws Exception {
        val session = request.getSession();
        if (session.getAttribute("lang") == null) {
            session.setAttribute("lang", "id");
            val sessionId = session.getId();
            val user = new User();
            user.setUserId(sessionId);
        }
        val query = request.getQueryString();
        if (query == null) {
            return true;
        }
        if (WAF.isMalicious(query)) {
            throw new HttpClientErrorException(HttpStatus.BAD_REQUEST, "Bad Request");
        }
        return true;
    }

}
