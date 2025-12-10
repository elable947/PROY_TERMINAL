CREATE OR ALTER PROCEDURE sp_EditarConductor
    @idConductorEmpresa INT,
    @idEmpresaTransporte INT,
    @licencia VARCHAR(50),
    @estado BIT
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @idUsuario INT;
    SELECT @idUsuario = idUsuario 
    FROM ConductorEmpresa 
    WHERE idConductorEmpresa = @idConductorEmpresa AND idEmpresaTransporte = @idEmpresaTransporte;

    IF @idUsuario IS NULL
    BEGIN
        THROW 51000, 'El conductor no pertenece a esta empresa o no existe.', 1;
    END

    BEGIN TRANSACTION;
    
    UPDATE ConductorEmpresa
    SET licencia = @licencia,
        estadoConductorEmpresa = @estado
    WHERE idConductorEmpresa = @idConductorEmpresa;

    COMMIT TRANSACTION;
END
