CREATE OR ALTER PROCEDURE sp_IniciarViaje
    @idViaje INT,
    @idUsuario INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Verify driver owns this trip
    IF EXISTS (
        SELECT 1 
        FROM Viaje v
        INNER JOIN ConductorEmpresa c ON v.idConductorEmpresa = c.idConductorEmpresa
        WHERE v.idViaje = @idViaje 
          AND c.idUsuario = @idUsuario
          AND v.idEstadoViaje = 1 -- Can only start if 'Disponible'
    )
    BEGIN
        UPDATE Viaje
        SET idEstadoViaje = 4 -- Set to 'En Ruta'
        WHERE idViaje = @idViaje;
        
        SELECT 1 as success, 'Viaje iniciado' as message;
    END
    ELSE
    BEGIN
        SELECT 0 as success, 'No se puede iniciar el viaje (no autorizado o estado incorrecto)' as message;
    END
END
