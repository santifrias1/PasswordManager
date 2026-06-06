package com.app.password_manager_backend.dto;

import lombok.Data;

@Data
public class AuthRequestDTO {
    private String username;
    private String masterPassword;
}