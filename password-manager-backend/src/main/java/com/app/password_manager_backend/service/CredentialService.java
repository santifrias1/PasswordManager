package com.app.password_manager_backend.service;

import com.app.password_manager_backend.model.Credential;
import com.app.password_manager_backend.model.User;
import com.app.password_manager_backend.repository.CredentialRepository;
import com.app.password_manager_backend.repository.UserRepository;
import com.app.password_manager_backend.security.CryptoUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class CredentialService {

    @Autowired
    private CredentialRepository credentialRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private CryptoUtils cryptoUtils;

    // Guardar una nueva credencial (Cifrando la contraseña)
    public Credential saveCredential(Long userId, String site, String username, String rawPassword, String notes) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("Usuario no encontrado"));

        Credential credential = new Credential();
        credential.setSite(site);
        credential.setUsername(username);
        credential.setNotes(notes);
        credential.setUser(user);
        
        // Cifrado simétrico AES
        credential.setEncryptedPassword(cryptoUtils.encryptAES(rawPassword));

        return credentialRepository.save(credential);
    }

    // Listar credenciales descifradas de un usuario
    public List<Credential> getCredentialsByUser(Long userId) {
        List<Credential> credentials = credentialRepository.findByUserId(userId);
        
        // Desciframos las contraseñas antes de enviarlas al flujo del frontend
        credentials.forEach(c -> {
            String decrypted = cryptoUtils.decryptAES(c.getEncryptedPassword());
            c.setEncryptedPassword(decrypted);
        });
        
        return credentials;
    }

    // Eliminar una credencial
    public void deleteCredential(Long credentialId) {
        if (!credentialRepository.existsById(credentialId)) {
            throw new RuntimeException("La credencial no existe.");
        }
        credentialRepository.deleteById(credentialId);
    }
}