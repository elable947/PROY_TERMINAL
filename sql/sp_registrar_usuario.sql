CREATE OR ALTER PROCEDURE sp_RegistrarUsuario
    @idTipoUsuario INT,
    @idPais INT,
    @nombre_usuario VARCHAR(255),
    @apPaterno VARCHAR(255),
    @apMaterno VARCHAR(255),
    @correo VARCHAR(255),
    @password VARCHAR(255),
    @telefono VARCHAR(50),
    @edad INT,
    @dni VARCHAR(15) = NULL,
    -- Linked Data
    @idEmpresaTransporte INT = NULL,
    @licencia VARCHAR(50) = NULL,
    @NewIdUsuario INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;

        -- Validar si el correo ya existe
        IF EXISTS (SELECT 1 FROM Usuario WHERE correo = @correo)
        BEGIN
            THROW 51000, 'El correo ya está registrado.', 1;
        END

        -- Validar si el usuario ya existe
        IF EXISTS (SELECT 1 FROM Usuario WHERE nombre_usuario = @nombre_usuario)
        BEGIN
            THROW 51000, 'El nombre de usuario ya está en uso.', 1;
        END

        -- Validar DNI si se provee
        IF @dni IS NOT NULL AND EXISTS (SELECT 1 FROM Usuario WHERE dni = @dni)
        BEGIN
            THROW 51000, 'El DNI ya está registrado.', 1;
        END

        -- Determine Status (1=Active by default, 0=Inactive for Role 2/4 requiring approval)
        DECLARE @esActivo BIT = 1;
        -- Now logic is: Admin assigns roles. So Register is always Pasajero (1).
        -- But keeping logic just in case backend sends 2/4.
        IF @idTipoUsuario IN (2, 4) 
            SET @esActivo = 0;

        -- Insertar Usuario (Now keeps DNI, Removed Licencia)
        INSERT INTO Usuario (idTipoUsuario, idPais, nombre_usuario, apPaterno, apMaterno, correo, password, telefono, esActivo, edad, dni)
        VALUES (@idTipoUsuario, @idPais, @nombre_usuario, @apPaterno, @apMaterno, @correo, @password, @telefono, @esActivo, @edad, @dni);

        SET @NewIdUsuario = SCOPE_IDENTITY();

        -- Si es Empresa (Tipo 2), LINK to existing Company
        IF @idTipoUsuario = 2
        BEGIN
            IF @idEmpresaTransporte IS NULL
            BEGIN
                THROW 51001, 'Debe seleccionar una empresa existente.', 1;
            END

            INSERT INTO UsuarioEmpresa (idUsuario, idEmpresaTransporte)
            VALUES (@NewIdUsuario, @idEmpresaTransporte);
        END

        -- Si es Conductor (Tipo 4), LINK to existing Company
        IF @idTipoUsuario = 4
        BEGIN
             IF @idEmpresaTransporte IS NULL
            BEGIN
                THROW 51001, 'Debe indicar empresa.', 1;
            END

            -- Note: ConductorEmpresa table columns: idUsuario, idEmpresaTransporte, licencia, fechaingreso, estadoConductorEmpresa
            INSERT INTO ConductorEmpresa (idUsuario, idEmpresaTransporte, licencia, fechaingreso, estadoConductorEmpresa)
            VALUES (@NewIdUsuario, @idEmpresaTransporte, @licencia, GETDATE(), 1); -- 'Pendiente' maps to 1? Or 0? Assuming 1 for now if registering directly.
        END

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
