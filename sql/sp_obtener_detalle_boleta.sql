CREATE OR ALTER PROCEDURE sp_ObtenerDetalleBoleta
    @idBoleto INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        b.idBoleto,
        b.fechaCompra,
        u.nombre_usuario,
        u.dni, 
        u.correo as email,
        v.fechaSalida,
        o.nombreTerminal as Origen,
        d.nombreDestino as Destino,
        et.nombreEmpresa,
        et.ruc,
        -- et.direccion, -- Removed as it does not exist
        ve.placa,
        tv.nombreTipoVehiculo as claseBus,
        a.numeroAsiento,
        v.precio,
        p.monto,
        mp.nombreMetodoPago,
        eb.nombreEstadoBoleto
    FROM Boleto b
    INNER JOIN Usuario u ON b.idUsuario = u.idUsuario
    INNER JOIN Viaje v ON b.idViaje = v.idViaje
    INNER JOIN Ruta r ON v.idRuta = r.idRuta
    INNER JOIN Terminal o ON r.idOrigen = o.idTerminal
    LEFT JOIN Destino d ON r.idDestino = d.idDestino
    INNER JOIN ConductorEmpresa ce ON v.idConductorEmpresa = ce.idConductorEmpresa
    INNER JOIN EmpresaTransporte et ON ce.idEmpresaTransporte = et.idEmpresaTransporte
    INNER JOIN Asiento a ON b.idAsiento = a.idAsiento
    INNER JOIN Vehiculo ve ON v.idVehiculo = ve.idVehiculo
    INNER JOIN TipoVehiculo tv ON ve.idTipoVehiculo = tv.idTipoVehiculo
    INNER JOIN EstadoBoleto eb ON b.idEstadoBoleto = eb.idEstadoBoleto
    LEFT JOIN Pago p ON p.idBoleto = b.idBoleto
    LEFT JOIN MetodoPago mp ON p.idMetodoPago = mp.idMetodoPago
    WHERE b.idBoleto = @idBoleto;
END
