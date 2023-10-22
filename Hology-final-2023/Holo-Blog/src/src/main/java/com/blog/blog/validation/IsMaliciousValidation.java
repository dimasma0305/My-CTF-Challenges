package com.blog.blog.validation;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

import com.blog.blog.waf.WAF;

public class IsMaliciousValidation implements ConstraintValidator<NotMalicious, String> {
    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        if (WAF.isMalicious(value)) {
            return false;
        }
        return true;
    }

}
