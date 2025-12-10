CREATE OR ALTER PROCEDURE sp_AsignarConductor
    @idUsuario INT,
    @idEmpresaTransporte INT,
    @licencia VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRANSACTION;

    -- Update User Role to Conductor (4)
    UPDATE Usuario
    SET idTipoUsuario = 4
    WHERE idUsuario = @idUsuario;
    
    -- Link Conductor to Company
    IF NOT EXISTS (SELECT 1 FROM ConductorEmpresa WHERE idUsuario = @idUsuario AND idEmpresaTransporte = @idEmpresaTransporte)
    BEGIN
        INSERT INTO ConductorEmpresa (idUsuario, idEmpresaTransporte, licencia, fechaingreso, estadoConductorEmpresa)
        VALUES (@idUsuario, @idEmpresaTransporte, @licencia, GETDATE(), 1);
    END
    ELSE
    BEGIN
        -- If exists (maybe inactive), reactivate and update license
        UPDATE ConductorEmpresa
        SET estadoConductorEmpresa = 1,
            licencia = @licencia,
            fechaingreso = GETDATE() -- Optional: Reset date or keep original? Keeping original usually better but updating for now implies new assignment
        WHERE idUsuario = @idUsuario AND idEmpresaTransporte = @idEmpresaTransporte;
    END

    COMMIT TRANSACTION;
END
