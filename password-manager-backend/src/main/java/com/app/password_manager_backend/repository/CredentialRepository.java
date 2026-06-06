package com.app.password_manager_backend.repository;

import com.app.password_manager_backend.model.Credential;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface CredentialRepository extends JpaRepository<Credential, Long> {
    // Recupera todas las credenciales asociadas al ID de un usuario específico
    List<Credential> findByUserId(Long userId);
}