CREATE OR ALTER PROCEDURE sp_ListarViajesConductor
    @idUsuario INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Get Conductor ID. 1 = Active.
    DECLARE @idConductorEmpresa INT;
    SELECT @idConductorEmpresa = idConductorEmpresa 
    FROM ConductorEmpresa 
    WHERE idUsuario = @idUsuario AND estadoConductorEmpresa = 1;

    IF @idConductorEmpresa IS NULL
    BEGIN
        -- Return empty result structure or nothing
        RETURN;
    END

    SELECT 
        v.idViaje,
        o.nombreDestino as Origen,
        d.nombreDestino as Destino,
        ve.placa,
        v.fechaSalida,
        v.precio,
        v.idEstadoViaje,
        v.asientosDisponibles, -- Also useful
        (SELECT COUNT(*) FROM Asiento WHERE idViaje = v.idViaje AND disponible = 0) as asientosOcupados,
        CASE v.idEstadoViaje
            WHEN 1 THEN 'Programado'
            WHEN 2 THEN 'En Curso'
            WHEN 3 THEN 'Finalizado'
            WHEN 4 THEN 'Cancelado'
            ELSE 'Desconocido'
        END as EstadoViaje
    FROM Viaje v
    INNER JOIN Ruta r ON v.idRuta = r.idRuta
    LEFT JOIN Destino o ON r.idOrigen = o.idDestino
    LEFT JOIN Destino d ON r.idDestino = d.idDestino
    INNER JOIN Vehiculo ve ON v.idVehiculo = ve.idVehiculo
    WHERE v.idConductorEmpresa = @idConductorEmpresa
    ORDER BY v.fechaSalida DESC;
END
