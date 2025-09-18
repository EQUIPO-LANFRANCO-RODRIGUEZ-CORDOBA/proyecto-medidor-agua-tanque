-- Crear base de datos
CREATE DATABASE IF NOT EXISTS esp32;
USE esp32;

-- Crear tabla para almacenar mediciones
CREATE TABLE IF NOT EXISTS NIVEL (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hora DATETIME NOT NULL,
    nivel VARCHAR(50) NOT NULL
);