CREATE OR ALTER PROCEDURE sp_EditarUsuario
    @idUsuario INT,
    @nombre_usuario VARCHAR(255),
    @apPaterno VARCHAR(255),
    @apMaterno VARCHAR(255),
    @correo VARCHAR(255),
    @telefono VARCHAR(50),
    @edad INT,
    @dni VARCHAR(15) = NULL,
    @idPais INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Check if new email exists for OTHER user
    IF EXISTS (SELECT 1 FROM Usuario WHERE correo = @correo AND idUsuario <> @idUsuario)
    BEGIN
        THROW 51000, 'El correo ya está en uso por otro usuario.', 1;
    END

    -- Check if new dni exists for OTHER user
    IF @dni IS NOT NULL AND EXISTS (SELECT 1 FROM Usuario WHERE dni = @dni AND idUsuario <> @idUsuario)
    BEGIN
        THROW 51000, 'El DNI ya está en uso por otro usuario.', 1;
    END

    UPDATE Usuario
    SET 
        nombre_usuario = @nombre_usuario,
        apPaterno = @apPaterno,
        apMaterno = @apMaterno,
        correo = @correo,
        telefono = @telefono,
        edad = @edad,
        dni = @dni,
        idPais = @idPais
    WHERE idUsuario = @idUsuario;
END
