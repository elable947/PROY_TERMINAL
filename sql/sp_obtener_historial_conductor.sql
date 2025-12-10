CREATE OR ALTER PROCEDURE sp_ObtenerHistorialViajesConductor
    @idUsuario INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Find driver ID
    DECLARE @idConductorEmpresa INT;
    SELECT @idConductorEmpresa = idConductorEmpresa 
    FROM ConductorEmpresa 
    WHERE idUsuario = @idUsuario; -- Removed active check to allow history even if currently inactive

    IF @idConductorEmpresa IS NULL
    BEGIN
        SELECT TOP 0 1 as idViaje; -- Return empty
        RETURN;
    END

    SELECT 
        v.idViaje,
        v.fechaSalida,
        ev.nombreEstadoViaje,
        ev.idEstadoViaje,
        o.nombreTerminal as origen,
        d.nombreDestino as destino,
        ve.placa
    FROM Viaje v
    INNER JOIN EstadoViaje ev ON v.idEstadoViaje = ev.idEstadoViaje
    INNER JOIN Ruta r ON v.idRuta = r.idRuta
    INNER JOIN Terminal o ON r.idOrigen = o.idTerminal
    INNER JOIN Destino d ON r.idDestino = d.idDestino
    INNER JOIN Vehiculo ve ON v.idVehiculo = ve.idVehiculo
    WHERE v.idConductorEmpresa = @idConductorEmpresa
      AND v.idEstadoViaje IN (2, 3) -- 2: Completado, 3: Cancelado
    ORDER BY v.fechaSalida DESC;
END
