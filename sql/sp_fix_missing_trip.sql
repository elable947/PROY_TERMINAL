CREATE OR ALTER PROCEDURE sp_ObtenerViajeActualConductor
    @idUsuario INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Find the driver record for this user (Status ANY, not just 1)
    -- We assume 1 driver record per user per company usually, or we take the one linked to the active trip.
    -- Better approach: Find the driver linked to an active trip first.
    
    DECLARE @idViaje INT;
    DECLARE @idConductorEmpresa INT;

    SELECT TOP 1 
        @idViaje = v.idViaje,
        @idConductorEmpresa = v.idConductorEmpresa
    FROM Viaje v
    INNER JOIN ConductorEmpresa c ON v.idConductorEmpresa = c.idConductorEmpresa
    WHERE c.idUsuario = @idUsuario 
      AND v.idEstadoViaje IN (1, 4) -- Scheduled or In Progress
    ORDER BY 
        CASE WHEN v.idEstadoViaje = 4 THEN 0 ELSE 1 END,
        v.fechaSalida ASC;

    -- If no trip found, return NULL
    IF @idViaje IS NULL
    BEGIN
        SELECT NULL as idViaje;
        RETURN;
    END

    -- Return full trip details
    SELECT 
        v.idViaje,
        v.fechaSalida,
        v.idEstadoViaje,
        ev.nombreEstadoViaje,
        r.duracionAprox,
        o.nombreTerminal as origen,
        d.nombreDestino as destino,
        ve.placa,
        ve.capacidadAsientos,
        (SELECT COUNT(*) 
         FROM Asiento a 
         WHERE a.idViaje = v.idViaje 
           AND (a.disponible = 0 OR a.disponible IS NULL)) as asientosOcupados
    FROM Viaje v
    INNER JOIN EstadoViaje ev ON v.idEstadoViaje = ev.idEstadoViaje
    INNER JOIN Ruta r ON v.idRuta = r.idRuta
    INNER JOIN Terminal o ON r.idOrigen = o.idTerminal
    INNER JOIN Destino d ON r.idDestino = d.idDestino
    INNER JOIN Vehiculo ve ON v.idVehiculo = ve.idVehiculo
    WHERE v.idViaje = @idViaje;
END
