CREATE OR ALTER PROCEDURE sp_FinalizarViaje
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
          AND v.idEstadoViaje = 4 -- Can only end if 'En Ruta'
    )
    BEGIN
        UPDATE Viaje
        SET idEstadoViaje = 2 -- Set to 'Completado'
        WHERE idViaje = @idViaje;
        
        SELECT 1 as success, 'Viaje finalizado' as message;
    END
    ELSE
    BEGIN
        SELECT 0 as success, 'No se puede finalizar el viaje (no autorizado o estado incorrecto)' as message;
    END
END
