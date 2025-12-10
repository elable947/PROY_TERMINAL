CREATE OR ALTER PROCEDURE sp_ListarDepartamentos
AS
BEGIN
    SET NOCOUNT ON;
    SELECT idDepartamento, nombreDepartamento FROM Departamento ORDER BY nombreDepartamento;
END
GO

CREATE OR ALTER PROCEDURE sp_ListarProvincias
    @idDepartamento INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT idProvincia, nombreProvincia FROM Provincia WHERE idDepartamento = @idDepartamento ORDER BY nombreProvincia;
END
GO

CREATE OR ALTER PROCEDURE sp_ListarDestinosPorProvincia
    @idProvincia INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT idDestino, nombreDestino FROM Destino WHERE idProvincia = @idProvincia ORDER BY nombreDestino;
END
GO

CREATE OR ALTER PROCEDURE sp_CrearDestino
    @idProvincia INT,
    @nombreDestino VARCHAR(255),
    @newId INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    IF EXISTS (SELECT 1 FROM Destino WHERE nombreDestino = @nombreDestino AND idProvincia = @idProvincia)
    BEGIN
        SELECT @newId = idDestino FROM Destino WHERE nombreDestino = @nombreDestino AND idProvincia = @idProvincia;
        RETURN;
    END

    INSERT INTO Destino (idProvincia, nombreDestino)
    VALUES (@idProvincia, @nombreDestino);
    
    SET @newId = SCOPE_IDENTITY();
END
GO

CREATE OR ALTER PROCEDURE sp_CrearRuta
    @idOrigen INT, -- Should be Chachapoyas ID by default
    @idDestino INT,
    @duracion VARCHAR(50),
    @distanciakm DECIMAL(10,2)
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Default to Chachapoyas Terminal (1) if null or 0
    IF @idOrigen IS NULL OR @idOrigen = 0 SET @idOrigen = 1;

    IF EXISTS (SELECT 1 FROM Ruta WHERE idOrigen = @idOrigen AND idDestino = @idDestino)
    BEGIN
        THROW 51000, 'Esta ruta ya existe.', 1;
    END

    INSERT INTO Ruta (idOrigen, idDestino, duracionAprox, distanciakm, estadoRuta)
    VALUES (@idOrigen, @idDestino, @duracion, @distanciakm, 1);
END
GO
