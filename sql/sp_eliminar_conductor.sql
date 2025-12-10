CREATE OR ALTER PROCEDURE sp_EliminarConductor
    @idConductorEmpresa INT,
    @idEmpresaTransporte INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Verify ownership
    DECLARE @idUsuario INT;
    SELECT @idUsuario = idUsuario 
    FROM ConductorEmpresa 
    WHERE idConductorEmpresa = @idConductorEmpresa AND idEmpresaTransporte = @idEmpresaTransporte;

    IF @idUsuario IS NULL
    BEGIN
        THROW 51000, 'El conductor no pertenece a esta empresa o no existe.', 1;
    END

    BEGIN TRANSACTION;

    -- Soft Delete in ConductorEmpresa (Bit 0 = Inactive)
    UPDATE ConductorEmpresa
    SET estadoConductorEmpresa = 0
    WHERE idConductorEmpresa = @idConductorEmpresa;

    -- Revert User Role to Pasajero (1)
    UPDATE Usuario
    SET idTipoUsuario = 1
    WHERE idUsuario = @idUsuario;

    COMMIT TRANSACTION;
END
