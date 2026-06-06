package com.app.password_manager_backend.service;

import com.app.password_manager_backend.repository.UserRepository;
import com.app.password_manager_backend.model.User;
import com.app.password_manager_backend.security.CryptoUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.Optional;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private CryptoUtils cryptoUtils;

    // Registro de usuario
    public User registerUser(String username, String rawMasterPassword) {
        if (userRepository.existsByUsername(username)) {
            throw new RuntimeException("El nombre de usuario ya existe.");
        }

        User user = new User();
        user.setUsername(username);
        // Hashear la contraseña maestra antes de guardarla
        user.setMasterPasswordHash(cryptoUtils.hashPassword(rawMasterPassword));

        return userRepository.save(user);
    }

    // Verificación de inicio de sesión
    public Optional<User> login(String username, String rawMasterPassword) {
        Optional<User> userOpt = userRepository.findByUsername(username);
        
        if (userOpt.isPresent()) {
            User user = userOpt.get();
            // Compara el texto plano enviado con el hash de la BD
            if (cryptoUtils.checkPassword(rawMasterPassword, user.getMasterPasswordHash())) {
                return Optional.of(user);
            }
        }
        return Optional.empty();
    }
}