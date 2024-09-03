-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS flask_app;

-- Usar la base de datos creada
USE flask_app;

-- Crear tabla 'hits' si no existe
CREATE TABLE IF NOT EXISTS hits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    count INT NOT NULL DEFAULT 0
);

-- Insertar un registro inicial en la tabla 'hits'
INSERT INTO hits (count) VALUES (0);

