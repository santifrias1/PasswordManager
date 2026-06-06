package com.app.password_manager_backend.dto;

import lombok.Data;

@Data
public class CredentialRequestDTO {
    private String site;
    private String username;
    private String password;
    private String notes;
}