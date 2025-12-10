CREATE OR ALTER PROCEDURE sp_ListarViajesEmpresa
    @idEmpresaTransporte INT
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        v.idViaje,
        v.fechaSalida,
        v.precio,
        v.asientosDisponibles,
        r.idRuta,
        t.nombreTerminal as Origen,
        d.nombreDestino as Destino,
        ve.placa,
        u.nombre_usuario as Conductor,
        ev.nombreEstadoViaje as Estado,
        ev.idEstadoViaje
    FROM Viaje v
    INNER JOIN Ruta r ON v.idRuta = r.idRuta
    INNER JOIN Terminal t ON r.idOrigen = t.idTerminal
    INNER JOIN Destino d ON r.idDestino = d.idDestino
    INNER JOIN Vehiculo ve ON v.idVehiculo = ve.idVehiculo
    INNER JOIN ConductorEmpresa c ON v.idConductorEmpresa = c.idConductorEmpresa
    INNER JOIN Usuario u ON c.idUsuario = u.idUsuario
    INNER JOIN EstadoViaje ev ON v.idEstadoViaje = ev.idEstadoViaje
    WHERE v.idEmpresaTransporte = @idEmpresaTransporte
    ORDER BY v.fechaSalida DESC;
END
