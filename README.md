# Local Password Manager

A secure credential management system developed using a decentralized client-server architecture. The application is designed to store, encrypt, and manage credentials locally while ensuring that sensitive information is never persisted in plain text.

---

## Overview

Local Password Manager is a full-stack desktop application that provides secure credential storage through a Python-based graphical client and a Spring Boot REST API. User authentication is protected using BCrypt hashing, while stored credentials are encrypted using AES before being persisted in PostgreSQL.

---

## System Architecture

The project follows a multi-tier architecture:

```text
Frontend (Python) → REST API (Spring Boot) → Database (PostgreSQL)
```

### Frontend

Graphical User Interface (GUI) built with `CustomTkinter`. The client communicates exclusively with the backend through HTTP requests.

### Backend

Developed with Java 21 and Spring Boot. Responsible for business logic, authentication, validation, encryption, and database interactions.

### Persistence Layer

PostgreSQL relational database managed through Spring Data JPA (Hibernate).

---

## Security and Encryption

The system prioritizes confidentiality through two complementary cryptographic mechanisms.

### Authentication (BCrypt)

User master passwords are hashed using BCrypt with a 12-round salt. The original password is never stored or retrievable.

### Credential Storage (AES)

Website credentials are encrypted using the AES algorithm before being persisted. Encryption and decryption operations are performed exclusively within the backend service layer.

---

## Core Features

* Secure user registration and authentication
* Credential CRUD operations
* Secure clipboard integration
* Built-in password generator
* Real-time credential search
* User-isolated credential storage
* RESTful architecture
* Local-first deployment model

---

## Technology Stack

### Backend

* Java 21
* Spring Boot 3
* Spring Web
* Spring Data JPA
* Hibernate
* Lombok
* jBCrypt
* Maven

### Frontend

* Python 3.13
* CustomTkinter
* Requests

### Database

* PostgreSQL 15+

### Development Tools

* Visual Studio Code
* DBeaver
* Git
* GitHub

---

# Repository Cloning

Clone the repository using SSH:

```bash
git clone git@github.com:santifrias1/PasswordManager.git
```

Move into the project directory:

```bash
cd PasswordManager
```

Alternatively, clone using HTTPS:

```bash
git clone https://github.com/santifrias1/PasswordManager.git
```

---

# Supported Platforms

The project has been tested on:

* Debian 13 (Trixie)
* OpenJDK 21
* PostgreSQL 15+
* Python 3.13
* Fish Shell 4.x

Other modern Linux distributions should work with minimal modifications.

---

# Platform-Specific Dependencies

## Debian / Ubuntu / Linux Mint

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib openjdk-21-jdk maven python3 python3-pip python3-venv
```

Verification:

```bash
java --version
mvn --version
python3 --version
psql --version
```

---

## Fedora

```bash
sudo dnf install postgresql-server postgresql java-21-openjdk maven python3 python3-pip
```

Initialize PostgreSQL:

```bash
sudo postgresql-setup --initdb
sudo systemctl enable --now postgresql
```

Verification:

```bash
java --version
mvn --version
python3 --version
psql --version
```

---

## Arch Linux

```bash
sudo pacman -Syu
sudo pacman -S postgresql jdk21-openjdk maven python python-pip
```

Initialize PostgreSQL:

```bash
sudo -iu postgres initdb --locale=C.UTF-8 -D /var/lib/postgres/data
sudo systemctl enable --now postgresql
```

Verification:

```bash
java --version
mvn --version
python --version
psql --version
```

---

## Alpine Linux

```bash
sudo apk update
sudo apk add postgresql postgresql-client openjdk21 maven python3 py3-pip py3-virtualenv
```

Initialize PostgreSQL:

```bash
sudo service postgresql setup
sudo rc-service postgresql start
sudo rc-update add postgresql
```

Verification:

```bash
java --version
mvn --version
python3 --version
psql --version
```

---

## Windows

Install the following software manually:

* PostgreSQL 15+
* Java Development Kit (JDK) 21
* Apache Maven
* Python 3.13+

Verification:

```powershell
java --version
mvn --version
python --version
psql --version
```

---

# Installation and Setup

## 1. Database Configuration

Create the PostgreSQL database:

```sql
CREATE DATABASE gestor_contrasenas;
```

The application uses the `postgres` account by default.

The following tables are generated automatically by Hibernate during backend startup:

* users
* credentials

Configuration:

```properties
spring.jpa.hibernate.ddl-auto=update
```

---

## 2. Environment Variables

Database credentials are injected through environment variables.

### Linux / macOS

```bash
export DB_USER=postgres
export DB_PASSWORD=your_password_here
```

### Fish Shell

```fish
set -x DB_USER postgres
set -x DB_PASSWORD your_password_here
```

### Windows PowerShell

```powershell
$env:DB_USER="postgres"
$env:DB_PASSWORD="your_password_here"
```

Verify the variables:

### Bash

```bash
echo $DB_USER
```

### Fish

```fish
echo $DB_USER
```

### PowerShell

```powershell
echo $env:DB_USER
```

---

## 3. Backend Deployment

Navigate to the backend directory:

```bash
cd password-manager-backend
```

Start the Spring Boot application.

### Linux / macOS

```bash
./mvnw spring-boot:run
```

### Windows

```powershell
.\mvnw.cmd spring-boot:run
```

The REST API will be available at:

```text
http://localhost:8080
```

---

## 4. Frontend Deployment

### Linux (Bash)

```bash
cd password-manager-gui

python3 -m venv venv
source venv/bin/activate

pip install customtkinter requests

python3 main.py
```

### Linux (Fish Shell)

```fish
cd password-manager-gui

python3 -m venv venv
source venv/bin/activate.fish

pip install customtkinter requests

python3 main.py
```

### Windows (PowerShell)

```powershell
cd password-manager-gui

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install customtkinter requests

python main.py
```

---

# Executable Compilation

The graphical client can be distributed as a standalone executable using PyInstaller.

> The backend service must still be running for authentication and data access.

Install PyInstaller:

```bash
pip install pyinstaller
```

Generate the executable:

```bash
pyinstaller --noconsole --onefile main.py
```

The compiled binary will be generated inside:

```text
dist/
```

---

# Project Structure

```text
PasswordManager/
├── password-manager-backend/
│   ├── src/main/java/com/app/password_manager_backend/
│   │   ├── controller/
│   │   ├── dto/
│   │   ├── model/
│   │   ├── repository/
│   │   ├── security/
│   │   ├── service/
│   │   └── PasswordManagerBackendApplication.java
│   └── src/main/resources/application.properties
│
└── password-manager-gui/
    └── main.py
```

---

## Backend Package Responsibilities

| Package    | Responsibility                           |
| ---------- | ---------------------------------------- |
| controller | REST API endpoints                       |
| dto        | Request and response DTOs                |
| model      | JPA entity definitions                   |
| repository | Data access layer                        |
| security   | AES encryption and BCrypt hashing        |
| service    | Business logic and application workflows |

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
