CREATE OR ALTER PROCEDURE sp_AsignarEmpresaUsuario
    @idUsuario INT,
    @idEmpresaTransporte INT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRANSACTION;
    
    -- Link User to Company
    IF NOT EXISTS (SELECT 1 FROM UsuarioEmpresa WHERE idUsuario = @idUsuario AND idEmpresaTransporte = @idEmpresaTransporte)
    BEGIN
        INSERT INTO UsuarioEmpresa (idUsuario, idEmpresaTransporte)
        VALUES (@idUsuario, @idEmpresaTransporte);
    END
    
    -- Promote User to 'Empresa' (2) if they are currently 'Pasajero' (1)
    -- This assumes Admin is designating a Manager.
    UPDATE Usuario
    SET idTipoUsuario = 2
    WHERE idUsuario = @idUsuario AND idTipoUsuario = 1;
    
    COMMIT TRANSACTION;
END
