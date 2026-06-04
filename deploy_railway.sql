
-- Eliminar tablas existentes (orden seguro por llaves foraneas) -------
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS cita;
DROP TABLE IF EXISTS horario_disponible;
DROP TABLE IF EXISTS medico_especialidad;
DROP TABLE IF EXISTS paciente;
DROP TABLE IF EXISTS administrativo;
DROP TABLE IF EXISTS medico;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS especialidad;
DROP TABLE IF EXISTS rol;
DROP TABLE IF EXISTS estado_usuario;
DROP TABLE IF EXISTS estado_medico;
DROP TABLE IF EXISTS estado_cita;
DROP TABLE IF EXISTS estado_horario_disponible;
SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================================
--  TABLAS DE CATALOGO / ESTADOS
-- =====================================================================
CREATE TABLE rol (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE estado_usuario (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE estado_medico (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE estado_cita (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE estado_horario_disponible (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- =====================================================================
--  ESPECIALIDAD  (incluye la imagen)
-- =====================================================================
CREATE TABLE especialidad (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    imagen      VARCHAR(255)        -- nombre del archivo en uploads/fotos/especialidades
) ENGINE=InnoDB;

-- =====================================================================
--  USUARIO  (autenticacion)
-- =====================================================================
CREATE TABLE usuario (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    email             VARCHAR(150) NOT NULL UNIQUE,
    password          VARCHAR(255) NOT NULL,   -- hash argon2
    rol_id            INT NOT NULL,
    estado_usuario_id INT NOT NULL,
    foto              VARCHAR(255),            -- archivo en uploads/fotos/usuarios
    CONSTRAINT fk_usuario_rol            FOREIGN KEY (rol_id)            REFERENCES rol(id),
    CONSTRAINT fk_usuario_estado_usuario FOREIGN KEY (estado_usuario_id) REFERENCES estado_usuario(id)
) ENGINE=InnoDB;

-- =====================================================================
--  PACIENTE
-- =====================================================================
CREATE TABLE paciente (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id       INT NOT NULL,
    nombres          VARCHAR(100) NOT NULL,
    apellidos        VARCHAR(100) NOT NULL,
    dni              VARCHAR(15),
    celular          VARCHAR(15),
    fecha_nacimiento DATE,
    genero           VARCHAR(20),
    CONSTRAINT fk_paciente_usuario FOREIGN KEY (usuario_id) REFERENCES usuario(id)
) ENGINE=InnoDB;

-- =====================================================================
--  MEDICO  (incluye la imagen, el horario y el consultorio)
-- =====================================================================
CREATE TABLE medico (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id       INT NOT NULL,
    nombres          VARCHAR(100) NOT NULL,
    apellidos        VARCHAR(100) NOT NULL,
    dni              VARCHAR(15),
    cmp              VARCHAR(20),
    telefono         VARCHAR(15),
    consultorio      VARCHAR(20),
    horario          VARCHAR(150),            -- texto descriptivo del horario de atencion
    foto             VARCHAR(255),            -- archivo en uploads/fotos/medicos
    estado_medico_id INT NOT NULL,
    CONSTRAINT fk_medico_usuario       FOREIGN KEY (usuario_id)       REFERENCES usuario(id),
    CONSTRAINT fk_medico_estado_medico FOREIGN KEY (estado_medico_id) REFERENCES estado_medico(id)
) ENGINE=InnoDB;

-- =====================================================================
--  ADMINISTRATIVO
-- =====================================================================
CREATE TABLE administrativo (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nombres    VARCHAR(100) NOT NULL,
    apellidos  VARCHAR(100) NOT NULL,
    dni        VARCHAR(15),
    celular    VARCHAR(15),
    cargo      VARCHAR(100),
    area       VARCHAR(100),
    CONSTRAINT fk_administrativo_usuario FOREIGN KEY (usuario_id) REFERENCES usuario(id)
) ENGINE=InnoDB;

-- =====================================================================
--  MEDICO_ESPECIALIDAD  (relacion muchos a muchos)
-- =====================================================================
CREATE TABLE medico_especialidad (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    medico_id       INT NOT NULL,
    especialidad_id INT NOT NULL,
    CONSTRAINT fk_me_medico       FOREIGN KEY (medico_id)       REFERENCES medico(id),
    CONSTRAINT fk_me_especialidad FOREIGN KEY (especialidad_id) REFERENCES especialidad(id)
) ENGINE=InnoDB;

-- =====================================================================
--  HORARIO_DISPONIBLE
-- =====================================================================
CREATE TABLE horario_disponible (
    id                            INT AUTO_INCREMENT PRIMARY KEY,
    medico_id                     INT NOT NULL,
    fecha                         DATE NOT NULL,
    hora_inicio                   TIME NOT NULL,
    hora_fin                      TIME NOT NULL,
    estado_horario_disponible_id  INT NOT NULL,
    CONSTRAINT fk_hd_medico FOREIGN KEY (medico_id) REFERENCES medico(id),
    CONSTRAINT fk_hd_estado FOREIGN KEY (estado_horario_disponible_id) REFERENCES estado_horario_disponible(id)
) ENGINE=InnoDB;

-- =====================================================================
--  CITA
-- =====================================================================
CREATE TABLE cita (
    id                     INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id            INT NOT NULL,
    horario_disponible_id  INT NOT NULL,
    motivo                 VARCHAR(255),
    paciente_oncologico    TINYINT(1) DEFAULT 0,
    estado_cita_id         INT NOT NULL,
    creado_por_usuario_id  INT NOT NULL,
    fecha_registro         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cita_paciente FOREIGN KEY (paciente_id)           REFERENCES paciente(id),
    CONSTRAINT fk_cita_horario  FOREIGN KEY (horario_disponible_id) REFERENCES horario_disponible(id),
    CONSTRAINT fk_cita_estado   FOREIGN KEY (estado_cita_id)        REFERENCES estado_cita(id),
    CONSTRAINT fk_cita_usuario  FOREIGN KEY (creado_por_usuario_id) REFERENCES usuario(id)
) ENGINE=InnoDB;

-- =====================================================================
--  DATOS DE PRUEBA (SEED)
-- =====================================================================

-- Catalogos --------------------------------------------------------
INSERT INTO rol (id, nombre) VALUES
    (1, 'paciente'),
    (2, 'medico'),
    (3, 'administrativo');

INSERT INTO estado_usuario (id, nombre) VALUES
    (1, 'activo'),
    (2, 'inactivo');

INSERT INTO estado_medico (id, nombre) VALUES
    (1, 'activo'),
    (2, 'inactivo');

INSERT INTO estado_cita (id, nombre) VALUES
    (1, 'pendiente'),
    (2, 'atendida'),
    (3, 'cancelada');

INSERT INTO estado_horario_disponible (id, nombre) VALUES
    (1, 'disponible'),
    (2, 'reservado');

-- Especialidades (las imagenes 1.png..5.png ya existen) ------------
INSERT INTO especialidad (id, nombre, descripcion, imagen) VALUES
    (1, 'Pediatría',    'Atención médica especializada para niños y adolescentes', '1.png'),
    (2, 'Cardiología',  'Diagnóstico y tratamiento de enfermedades del corazón',   '2.png'),
    (3, 'Dermatología', 'Atención integral en enfermedades y cuidados de la piel',  '3.png'),
    (4, 'Neurología',   'Atención especializada en trastornos del sistema nervioso','4.png'),
    (5, 'Oftalmología', 'Diagnóstico y tratamiento de enfermedades de la vista',    '5.png');

-- Usuarios (contrasena de todos: usat) -----------------------------
INSERT INTO usuario (id, email, password, rol_id, estado_usuario_id, foto) VALUES
    (1, 'admin@clinica.com',          '$argon2id$v=19$m=65536,t=3,p=4$kyLyxNmkSdZTQ1jHMmZ6lQ$IlaY9/Xdg00dAz+u+z0ryFGFyGbN0su2138Hd/rU+1c', 3, 1, NULL),
    (2, 'ana.torres@gmail.com',       '$argon2id$v=19$m=65536,t=3,p=4$a3jTwj1l1zKtEMv9mOpTZQ$JH3zqgzjNfnHAeCKih2RMaI0V3rVWpxsNhTcR8oMIDc', 1, 1, NULL),
    (3, 'maria.lopez@clinica.com',    '$argon2id$v=19$m=65536,t=3,p=4$5MjgP7afGD88DcEs/HX3Vg$8+b1RH7HO0GlcMPKTEkwMcQtVerOl1IlQ7y2RSVKl9o', 2, 1, NULL),
    (4, 'jose.rivera@clinica.com',    '$argon2id$v=19$m=65536,t=3,p=4$9W/6GwRWC4V4DCclIkS9UQ$0Q66oqJcxwespRy1twLgZnAy5D0gKo3aS3qUVjaR0gY', 2, 1, NULL),
    (5, 'carlos.ramirez@clinica.com', '$argon2id$v=19$m=65536,t=3,p=4$Ae7JThda/OChvoTZ+pri9Q$XY7WzD76eKw0VzusKC756Eo1hcbud0bM81OOinit4pg', 2, 1, NULL),
    (6, 'andrea.castillo@clinica.com','$argon2id$v=19$m=65536,t=3,p=4$mVjhI1CChTIPZ283UerSJg$DxYMCPo0eO1o7UiTO8QJzooMVBs1l1xbQSTs9nGNQZ8', 2, 1, NULL);

-- Paciente ---------------------------------------------------------
INSERT INTO paciente (id, usuario_id, nombres, apellidos, dni, celular, fecha_nacimiento, genero) VALUES
    (1, 2, 'Ana', 'Torres Díaz', '70123456', '999888777', '2000-05-10', 'Femenino');

-- Administrativo ---------------------------------------------------
INSERT INTO administrativo (id, usuario_id, nombres, apellidos, dni, celular, cargo, area) VALUES
    (1, 1, 'Lucía', 'Campos Ruiz', '73322110', '944555666', 'Recepcionista', 'Admisión');

-- Medicos (las imagenes 1.png..4.png ya existen en uploads/fotos/medicos)
INSERT INTO medico (id, usuario_id, nombres, apellidos, dni, cmp, telefono, consultorio, horario, foto, estado_medico_id) VALUES
    (1, 3, 'María',  'López',    '70112233', 'CMP1001', '999111222', '101', 'Lunes a Viernes - 8:00 a.m. a 1:00 p.m.',          '1.png', 1),
    (2, 4, 'José',   'Rivera',   '70112244', 'CMP1002', '999111333', '102', 'Lunes, Miércoles y Viernes - 2:00 p.m. a 6:00 p.m.','2.png', 1),
    (3, 5, 'Carlos', 'Ramírez',  '70112255', 'CMP1003', '999111444', '202', 'Lunes, Miércoles y Viernes - 3:00 p.m. a 7:00 p.m.','3.png', 1),
    (4, 6, 'Andrea', 'Castillo', '70112266', 'CMP1004', '999111555', '203', 'Martes y Jueves - 9:00 a.m. a 2:00 p.m.',          '4.png', 1);

-- Relacion medico - especialidad -----------------------------------
INSERT INTO medico_especialidad (id, medico_id, especialidad_id) VALUES
    (1, 1, 1),   -- María López    -> Pediatría
    (2, 2, 1),   -- José Rivera    -> Pediatría
    (3, 3, 2),   -- Carlos Ramírez -> Cardiología
    (4, 4, 3);   -- Andrea Castillo-> Dermatología

-- Horarios disponibles (para registrar citas) ----------------------
INSERT INTO horario_disponible (id, medico_id, fecha, hora_inicio, hora_fin, estado_horario_disponible_id) VALUES
    (1, 1, '2026-06-10', '08:00:00', '08:30:00', 1),
    (2, 1, '2026-06-10', '08:30:00', '09:00:00', 1),
    (3, 3, '2026-06-11', '15:00:00', '15:30:00', 1),
    (4, 4, '2026-06-12', '09:00:00', '09:30:00', 1);

-- =====================================================================
--  FIN
-- =====================================================================
