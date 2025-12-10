CREATE OR ALTER PROCEDURE sp_ObtenerViajeActualConductor
    @idUsuario INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Find the active driver record for this user
    DECLARE @idConductorEmpresa INT;
    SELECT @idConductorEmpresa = idConductorEmpresa 
    FROM ConductorEmpresa 
    WHERE idUsuario = @idUsuario AND estadoConductorEmpresa = 1;

    IF @idConductorEmpresa IS NULL
    BEGIN
        SELECT NULL as idViaje;
        RETURN;
    END

    -- Find active trip (Scheduled=1 or In Progress=4)
    SELECT TOP 1 
        v.idViaje,
        v.fechaSalida,
        v.idEstadoViaje,
        ev.nombreEstadoViaje,
        r.duracionAprox,
        o.nombreTerminal as origen,
        d.nombreDestino as destino,
        ve.placa,
        ve.capacidadAsientos,
        -- Count occupied seats (Assuming 'disponible' = 0 means occupied)
        -- We check Asiento table. If row exists and disponible=0, it's taken.
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
    WHERE v.idConductorEmpresa = @idConductorEmpresa
      AND v.idEstadoViaje IN (1, 4)
    ORDER BY 
        CASE WHEN v.idEstadoViaje = 4 THEN 0 ELSE 1 END,
        v.fechaSalida ASC;
END
