CREATE OR ALTER PROCEDURE sp_ObtenerHistorialUsuario
    @idUsuario INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        b.idBoleto,
        b.fechaCompra,
        b.idEstadoBoleto,
        eb.nombreEstadoBoleto,
        v.fechaSalida,
        v.precio,
        o.nombreDestino as Origen,
        d.nombreDestino as Destino,
        et.nombreEmpresa,
        et.ruc,
        a.numeroAsiento,
        ve.placa,
        tv.nombreTipoVehiculo as claseBus,
        mp.nombreMetodoPago
    FROM Boleto b
    INNER JOIN Viaje v ON b.idViaje = v.idViaje
    INNER JOIN Ruta r ON v.idRuta = r.idRuta
    INNER JOIN Destino o ON r.idOrigen = o.idDestino
    LEFT JOIN Destino d ON r.idDestino = d.idDestino
    INNER JOIN ConductorEmpresa ce ON v.idConductorEmpresa = ce.idConductorEmpresa
    INNER JOIN EmpresaTransporte et ON ce.idEmpresaTransporte = et.idEmpresaTransporte
    INNER JOIN Asiento a ON b.idAsiento = a.idAsiento
    INNER JOIN Vehiculo ve ON v.idVehiculo = ve.idVehiculo
    INNER JOIN TipoVehiculo tv ON ve.idTipoVehiculo = tv.idTipoVehiculo
    INNER JOIN EstadoBoleto eb ON b.idEstadoBoleto = eb.idEstadoBoleto
    LEFT JOIN Pago p ON p.idBoleto = b.idBoleto 
    LEFT JOIN MetodoPago mp ON p.idMetodoPago = mp.idMetodoPago
    WHERE b.idUsuario = @idUsuario
    ORDER BY b.fechaCompra DESC;
END
