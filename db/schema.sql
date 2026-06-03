-- Job Portal DB Schema
CREATE DATABASE IF NOT EXISTS jobportal_db;
USE jobportal_db;

CREATE TABLE users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role          ENUM('seeker','employer','admin') DEFAULT 'seeker',
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);

CREATE TABLE companies (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL UNIQUE,
    name        VARCHAR(150) NOT NULL,
    description TEXT,
    website     VARCHAR(200),
    location    VARCHAR(100),
    logo_path   VARCHAR(255),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE job_listings (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    company_id  INT NOT NULL,
    title       VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    location    VARCHAR(100),
    salary      DECIMAL(10,2) DEFAULT 0,
    category    VARCHAR(80),
    deadline    DATE NOT NULL,
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    INDEX idx_category (category),
    INDEX idx_deadline (deadline)
);

CREATE TABLE applications (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    job_id      INT NOT NULL,
    status      ENUM('pending','shortlisted','rejected') DEFAULT 'pending',
    resume_path VARCHAR(255),
    applied_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id)  REFERENCES job_listings(id) ON DELETE CASCADE,
    UNIQUE KEY uq_application (user_id, job_id)
);

CREATE TABLE skills (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT NOT NULL,
    skill_name VARCHAR(80) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Seed admin user (password: admin123)
INSERT INTO users (name, email, password_hash, role) VALUES
('Admin', 'admin@jobportal.com',
 '$2b$12$KIXTMzENQhh8.xd7Xk8tWOxF7GJM4LWbq5rGz1pBBpAb2.qGp0kgq', 'admin');
