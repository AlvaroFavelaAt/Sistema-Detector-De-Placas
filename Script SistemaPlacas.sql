CREATE DATABASE SistemaPlacas;
GO
USE SistemaPlacas;
GO

-- TABLA DE PROPIETARIOS
CREATE TABLE Propietarios (
    id_propietario INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    direccion VARCHAR(150)
);

-- TABLA DE VEHÍCULOS
CREATE TABLE Vehiculos (
    id_vehiculo INT IDENTITY(1,1) PRIMARY KEY,
    placa VARCHAR(20) NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    año INT,
    id_propietario INT,
    fecha_registro DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (id_propietario) REFERENCES Propietarios(id_propietario)
);



SELECT * FROM Propietarios;
SELECT * FROM Vehiculos;

DROP DATABASE SistemaPlacas;
