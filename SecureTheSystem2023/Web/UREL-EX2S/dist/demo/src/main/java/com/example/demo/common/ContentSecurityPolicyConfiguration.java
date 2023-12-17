package com.example.demo.common;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class ContentSecurityPolicyConfiguration {
    @Bean
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http.headers(headers -> {
            headers.xssProtection();
            headers.contentSecurityPolicy("default-src https://unpkg.com https://cdn.tailwindcss.com 'unsafe-eval' 'unsafe-inline' 'self'; object-src 'none';");
        });
        return http.build();
    }
}
