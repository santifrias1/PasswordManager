package com.app.password_manager_backend.controller;

import com.app.password_manager_backend.dto.AuthRequestDTO;
import com.app.password_manager_backend.model.User;
import com.app.password_manager_backend.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody AuthRequestDTO request) {
        try {
            User newUser = userService.registerUser(request.getUsername(), request.getMasterPassword());
            return new ResponseEntity<>("Usuario registrado exitosamente con ID: " + newUser.getId(), HttpStatus.CREATED);
        } catch (RuntimeException e) {
            return new ResponseEntity<>(e.getMessage(), HttpStatus.BAD_REQUEST);
        }
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody AuthRequestDTO request) {
        Optional<User> user = userService.login(request.getUsername(), request.getMasterPassword());
        
        if (user.isPresent()) {
            // En una app real con JWT devolveríamos un token aquí. 
            // Para este proyecto local, devolvemos el ID del usuario para que el frontend Python lo guarde en sesión.
            return new ResponseEntity<>(user.get().getId(), HttpStatus.OK);
        } else {
            return new ResponseEntity<>("Credenciales inválidas", HttpStatus.UNAUTHORIZED);
        }
    }
}