package com.blog.blog.validation;

import javax.validation.constraints.NotNull;

import lombok.Data;

@Data
public class Lang {
    @NotNull
    @NotMalicious
    private String lang;
}
