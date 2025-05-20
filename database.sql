-- Tabla de Carreras
CREATE TABLE Carreras (
    ID_carrera INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL
);

-- Tabla de Usuarios
CREATE TABLE Usuarios (
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
);

-- Tabla de Profesores
CREATE TABLE Profesores (
    ID_profesor INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100),
    Departamento VARCHAR(100)
);

-- Tabla de Materias
CREATE TABLE Materias (
    ID_materia INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100),
    ID_carrera INT,
    Semestre_sugerido INT,
    ID_profesor_encargado INT,
    FOREIGN KEY (ID_carrera) REFERENCES Carreras(ID_carrera),
    FOREIGN KEY (ID_profesor_encargado) REFERENCES Profesores(ID_profesor)
);

-- Tabla de Cursos (Grupos)
CREATE TABLE Cursos (
    ID_curso INT AUTO_INCREMENT PRIMARY KEY,
    ID_materia INT,
    Semestre INT,
    ID_profesor INT,
    Horario VARCHAR(100),
    Ubicacion VARCHAR(100),
    FOREIGN KEY (ID_materia) REFERENCES Materias(ID_materia),
    FOREIGN KEY (ID_profesor) REFERENCES Profesores(ID_profesor)
);

-- Tabla de Evaluaciones de Profesores
CREATE TABLE Evaluaciones (
    ID_evaluacion INT AUTO_INCREMENT PRIMARY KEY,
    ID_profesor INT,
    ID_usuario INT,
    Estrellas INT CHECK (Estrellas >= 1 AND Estrellas <= 5),
    Comentario TEXT,
    Fecha DATE,
    FOREIGN KEY (ID_profesor) REFERENCES Profesores(ID_profesor),
    FOREIGN KEY (ID_usuario) REFERENCES Usuarios(ID_usuario)
);

-- Tabla de Foros de Materia
CREATE TABLE Foros (
    ID_foro INT AUTO_INCREMENT PRIMARY KEY,
    ID_materia INT,
    ID_curso INT,
    FOREIGN KEY (ID_materia) REFERENCES Materias(ID_materia),
    FOREIGN KEY (ID_curso) REFERENCES Cursos(ID_curso)
);

-- Tabla de Publicaciones en Foros
CREATE TABLE Publicaciones_Foro (
    ID_publicacion INT AUTO_INCREMENT PRIMARY KEY,
    ID_foro INT,
    ID_usuario INT,
    Titulo VARCHAR(100),
    Contenido TEXT,
    Fecha DATE,
    FOREIGN KEY (ID_foro) REFERENCES Foros(ID_foro),
    FOREIGN KEY (ID_usuario) REFERENCES Usuarios(ID_usuario)
);

-- Tabla de Comunidad Estudiantil
CREATE TABLE Comunidad_Estudantil (
    ID_publicacion INT AUTO_INCREMENT PRIMARY KEY,
    ID_usuario INT,
    Titulo VARCHAR(100),
    Contenido TEXT,
    Categoria VARCHAR(50),
    Fecha DATE,
    FOREIGN KEY (ID_usuario) REFERENCES Usuarios(ID_usuario)
);

-- Tabla de Mapa Interactivo
CREATE TABLE Mapa_Interactivo (
    ID_ubicacion INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_edificio VARCHAR(100),
    Piso VARCHAR(10),
    Salon VARCHAR(50),
    ID_curso INT,
    FOREIGN KEY (ID_curso) REFERENCES Cursos(ID_curso)
);
