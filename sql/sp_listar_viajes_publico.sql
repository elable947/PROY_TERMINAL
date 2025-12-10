CREATE OR ALTER PROCEDURE sp_ListarViajesPublico
    @idDestino INT = NULL,
    @idEmpresa INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        v.idViaje,
        v.fechaSalida,
        v.precio,
        v.idEstadoViaje,
        et.nombreEmpresa,
        et.idEmpresaTransporte,
        t.nombreTerminal as origen,
        d.nombreDestino as destino,
        tv.nombreTipoVehiculo as clase,
        r.duracionAprox,
        r.distanciakm,
        ve.placa,
        ve.capacidadAsientos,
        (ve.capacidadAsientos - ISNULL((SELECT COUNT(*) FROM Asiento a WHERE a.idViaje = v.idViaje AND (a.disponible = 0 OR a.disponible IS NULL)), 0)) as asientosDisponibles
    FROM Viaje v
    INNER JOIN Ruta r ON v.idRuta = r.idRuta
    INNER JOIN Terminal t ON r.idOrigen = t.idTerminal
    INNER JOIN Destino d ON r.idDestino = d.idDestino
    INNER JOIN Vehiculo ve ON v.idVehiculo = ve.idVehiculo
    INNER JOIN TipoVehiculo tv ON ve.idTipoVehiculo = tv.idTipoVehiculo
    INNER JOIN EmpresaTransporte et ON v.idEmpresaTransporte = et.idEmpresaTransporte
    WHERE v.idEstadoViaje = 1 -- Programado
      AND v.fechaSalida >= GETDATE()
      AND (@idDestino IS NULL OR d.idDestino = @idDestino)
      AND (@idEmpresa IS NULL OR et.idEmpresaTransporte = @idEmpresa)
    ORDER BY v.fechaSalida ASC;
END
