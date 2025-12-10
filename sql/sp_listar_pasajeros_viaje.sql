CREATE OR ALTER PROCEDURE sp_ListarPasajerosViaje
    @idViaje INT,
    @idUsuarioConductor INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Verify driver is assigned to this trip
    DECLARE @idConductorEmpresa INT;
    SELECT @idConductorEmpresa = idConductorEmpresa 
    FROM ConductorEmpresa 
    WHERE idUsuario = @idUsuarioConductor;

    IF EXISTS (SELECT 1 FROM Viaje WHERE idViaje = @idViaje AND idConductorEmpresa = @idConductorEmpresa)
    BEGIN
        SELECT 
            a.numeroAsiento,
            u.nombre_usuario + ' ' + ISNULL(u.apPaterno, '') as Pasajero,
            u.dni,
            o.nombreTerminal as Origen,
            d.nombreDestino as Destino,
            eb.nombreEstadoBoleto as Estado
        FROM Boleto b
        INNER JOIN Usuario u ON b.idUsuario = u.idUsuario
        INNER JOIN Asiento a ON b.idAsiento = a.idAsiento
        INNER JOIN EstadoBoleto eb ON b.idEstadoBoleto = eb.idEstadoBoleto
        INNER JOIN Viaje v ON b.idViaje = v.idViaje
        INNER JOIN Ruta r ON v.idRuta = r.idRuta
        INNER JOIN Terminal o ON r.idOrigen = o.idTerminal
        LEFT JOIN Destino d ON r.idDestino = d.idDestino
        WHERE b.idViaje = @idViaje
          AND b.idEstadoBoleto IN (1, 2) -- Show Reserved (1) and Paid (2)
        ORDER BY a.numeroAsiento;
    END
    ELSE
    BEGIN
        -- Return empty if not authorized
        SELECT 1 WHERE 1=0; 
    END
END
