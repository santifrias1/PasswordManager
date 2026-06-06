package com.app.password_manager_backend.controller;

import com.app.password_manager_backend.dto.CredentialRequestDTO;
import com.app.password_manager_backend.model.Credential;
import com.app.password_manager_backend.service.CredentialService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/credentials")
public class CredentialController {

    @Autowired
    private CredentialService credentialService;

    // Guardar una nueva credencial asociada a un usuario
    @PostMapping("/{userId}")
    public ResponseEntity<?> saveCredential(@PathVariable Long userId, @RequestBody CredentialRequestDTO request) {
        try {
            Credential saved = credentialService.saveCredential(
                    userId, 
                    request.getSite(), 
                    request.getUsername(), 
                    request.getPassword(), 
                    request.getNotes()
            );
            return new ResponseEntity<>(saved, HttpStatus.CREATED);
        } catch (RuntimeException e) {
            return new ResponseEntity<>(e.getMessage(), HttpStatus.BAD_REQUEST);
        }
    }

    // Obtener todas las credenciales (ya descifradas) de un usuario
    @GetMapping("/{userId}")
    public ResponseEntity<List<Credential>> getCredentials(@PathVariable Long userId) {
        List<Credential> credentials = credentialService.getCredentialsByUser(userId);
        return new ResponseEntity<>(credentials, HttpStatus.OK);
    }

    // Eliminar una credencial específica
    @DeleteMapping("/{credentialId}")
    public ResponseEntity<?> deleteCredential(@PathVariable Long credentialId) {
        try {
            credentialService.deleteCredential(credentialId);
            return new ResponseEntity<>("Credencial eliminada", HttpStatus.OK);
        } catch (RuntimeException e) {
            return new ResponseEntity<>(e.getMessage(), HttpStatus.NOT_FOUND);
        }
    }
}