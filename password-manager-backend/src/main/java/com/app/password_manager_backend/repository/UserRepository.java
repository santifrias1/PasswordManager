package com.app.password_manager_backend.repository;

import com.app.password_manager_backend.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    // Método para buscar un usuario por su username
    Optional<User> findByUsername(String username);
    
    // Método para verificar si un username ya existe (útil en el registro)
    boolean existsByUsername(String username);
}