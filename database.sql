create database respaldo;
use respaldo;
-- Desactivar restricciones temporales
SET FOREIGN_KEY_CHECKS = 0;

-- Tabla: Facultades
CREATE TABLE IF NOT EXISTS Facultades (
    ID_facultad INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla: Carreras
CREATE TABLE IF NOT EXISTS Carreras (
    ID_carrera INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    ID_facultad INT,
    FOREIGN KEY (ID_facultad) REFERENCES Facultades(ID_facultad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla: Usuarios
CREATE TABLE IF NOT EXISTS Usuarios (
    ID_usuario INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100),
    Apellido VARCHAR(100),
    Correo_institucional VARCHAR(100) UNIQUE,
    Contrasena VARCHAR(255),
    Foto_perfil TEXT,
    Fecha_registro DATE,
    Semestre INT,
    Semillero VARCHAR(100),
    ID_carrera INT,
    FOREIGN KEY (ID_carrera) REFERENCES Carreras(ID_carrera)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla: Profesores
CREATE TABLE IF NOT EXISTS Profesores (
    ID_profesor INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Correo_institucional VARCHAR(100) UNIQUE NOT NULL,
    ID_facultad INT,
    FOREIGN KEY (ID_facultad) REFERENCES Facultades(ID_facultad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla: Materias
CREATE TABLE IF NOT EXISTS Materias (
    ID_materia INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Codigo VARCHAR(20) NOT NULL UNIQUE,
    ID_facultad INT,
    FOREIGN KEY (ID_facultad) REFERENCES Facultades(ID_facultad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla: Cursos (Grupos)
CREATE TABLE IF NOT EXISTS Cursos (
    ID_curso INT AUTO_INCREMENT PRIMARY KEY,
    ID_materia INT,
    ID_profesor INT,
    Semestre VARCHAR(10),
    Grupo VARCHAR(10),
    FOREIGN KEY (ID_materia) REFERENCES Materias(ID_materia),
    FOREIGN KEY (ID_profesor) REFERENCES Profesores(ID_profesor)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla: Evaluaciones
CREATE TABLE IF NOT EXISTS Evaluaciones (
    ID_evaluacion INT AUTO_INCREMENT PRIMARY KEY,
    ID_profesor INT NOT NULL,
    ID_usuario INT NOT NULL,
    Estrellas TINYINT NOT NULL CHECK (Estrellas BETWEEN 1 AND 5),
    Comentario TEXT,
    Fecha DATE,
    UNIQUE KEY (ID_profesor, ID_usuario),
    FOREIGN KEY (ID_profesor) REFERENCES Profesores(ID_profesor) ON DELETE CASCADE,
    FOREIGN KEY (ID_usuario) REFERENCES Usuarios(ID_usuario) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla: Foros
CREATE TABLE IF NOT EXISTS Foros (
    ID_foro INT AUTO_INCREMENT PRIMARY KEY,
    ID_materia INT,
    ID_curso INT,
    FOREIGN KEY (ID_materia) REFERENCES Materias(ID_materia),
    FOREIGN KEY (ID_curso) REFERENCES Cursos(ID_curso)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla: Publicaciones en Foros
CREATE TABLE IF NOT EXISTS Publicaciones_Foro (
    ID_publicacion INT AUTO_INCREMENT PRIMARY KEY,
    ID_foro INT,
    ID_usuario INT,
    Titulo VARCHAR(100),
    Contenido TEXT,
    Fecha DATE,
    FOREIGN KEY (ID_foro) REFERENCES Foros(ID_foro),
    FOREIGN KEY (ID_usuario) REFERENCES Usuarios(ID_usuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla: Comunidad Estudiantil
CREATE TABLE IF NOT EXISTS Comunidad_Estudantil (
    ID_publicacion INT AUTO_INCREMENT PRIMARY KEY,
    ID_usuario INT,
    Titulo VARCHAR(100),
    Contenido TEXT,
    Categoria VARCHAR(50),
    Fecha DATE,
    FOREIGN KEY (ID_usuario) REFERENCES Usuarios(ID_usuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla: Mapa Interactivo
CREATE TABLE IF NOT EXISTS Mapa_Interactivo (
    ID_ubicacion INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_edificio VARCHAR(100),
    Piso VARCHAR(10),
    Salon VARCHAR(50),
    ID_curso INT,
    FOREIGN KEY (ID_curso) REFERENCES Cursos(ID_curso)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla intermedia: Profesores-Materias
CREATE TABLE IF NOT EXISTS Profesores_Materias (
    ID_profesor INT NOT NULL,
    ID_materia INT NOT NULL,
    PRIMARY KEY (ID_profesor, ID_materia),
    FOREIGN KEY (ID_profesor) REFERENCES Profesores(ID_profesor) ON DELETE CASCADE,
    FOREIGN KEY (ID_materia) REFERENCES Materias(ID_materia) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Activar de nuevo restricciones
SET FOREIGN_KEY_CHECKS = 1;
