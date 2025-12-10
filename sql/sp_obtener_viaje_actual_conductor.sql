CREATE OR ALTER PROCEDURE sp_ObtenerViajeActualConductor
    @idUsuario INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Get Conductor
    DECLARE @idConductorEmpresa INT;
    SELECT @idConductorEmpresa = idConductorEmpresa 
    FROM ConductorEmpresa 
    WHERE idUsuario = @idUsuario AND estadoConductorEmpresa = 1;

    IF @idConductorEmpresa IS NULL RETURN;

    -- Select *Current* trip (Scheduled or In Progress)
    -- Order by date ASC to get the 'next' or 'active' one? 
    -- Or just TOP 1 
    SELECT TOP 1
        v.idViaje,
        o.nombreTerminal as origen,
        d.nombreDestino as destino,
        ve.placa,
        ve.capacidadAsientos,
        v.fechaSalida,
        v.precio,
        v.idEstadoViaje,
        v.asientosDisponibles,
        (SELECT COUNT(*) FROM Asiento WHERE idViaje = v.idViaje AND disponible = 0) as asientosOcupados,
        CASE v.idEstadoViaje
            WHEN 1 THEN 'Programado'
            WHEN 4 THEN 'En Ruta'
            ELSE 'Desconocido'
        END as nombreEstadoViaje
    FROM Viaje v
    INNER JOIN Ruta r ON v.idRuta = r.idRuta
    LEFT JOIN Terminal o ON r.idOrigen = o.idTerminal
    LEFT JOIN Destino d ON r.idDestino = d.idDestino
    INNER JOIN Vehiculo ve ON v.idVehiculo = ve.idVehiculo
    WHERE v.idConductorEmpresa = @idConductorEmpresa
      AND v.idEstadoViaje IN (1, 4) -- Only Scheduled or In Progress
    ORDER BY 
        CASE WHEN v.idEstadoViaje = 4 THEN 0 ELSE 1 END, -- Prioritize 'En Ruta'
        v.fechaSalida ASC;
END
