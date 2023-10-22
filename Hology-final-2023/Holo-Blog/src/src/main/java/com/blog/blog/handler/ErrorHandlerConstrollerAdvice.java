package com.blog.blog.handler;

import java.sql.SQLException;
import javax.servlet.http.HttpServletResponse;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.client.HttpClientErrorException;
import com.blog.blog.controler.DefaultResponseFormat;

@ControllerAdvice
public class ErrorHandlerConstrollerAdvice {
    @ExceptionHandler(HttpClientErrorException.class)
    @ResponseBody
    DefaultResponseFormat onHttpClientErrorException(HttpClientErrorException e, HttpServletResponse response) {
        response.setStatus(e.getStatusCode().value());
        DefaultResponseFormat defaultResponseFormat = new DefaultResponseFormat();
        defaultResponseFormat.setMessage(e.getMessage());
        return defaultResponseFormat;
    }

    @ExceptionHandler(SQLException.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    @ResponseBody
    DefaultResponseFormat onSQLException(SQLException e, HttpServletResponse response) {
        DefaultResponseFormat defaultResponseFormat = new DefaultResponseFormat();
        defaultResponseFormat.setMessage(e.getMessage());
        return defaultResponseFormat;
    }

    @ExceptionHandler(IllegalArgumentException.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    @ResponseBody
    DefaultResponseFormat onIllegalArgumentException(IllegalArgumentException e, HttpServletResponse response) {
        DefaultResponseFormat defaultResponseFormat = new DefaultResponseFormat();
        defaultResponseFormat.setMessage(e.getMessage());
        return defaultResponseFormat;
    }
}
