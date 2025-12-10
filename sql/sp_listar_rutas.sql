CREATE OR ALTER PROCEDURE sp_ListarRutas
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        r.idRuta,
        t.nombreTerminal as Origen,
        d.nombreDestino as Destino,
        r.duracionAprox,
        r.distanciakm,
        r.estadoRuta
    FROM Ruta r
    INNER JOIN Terminal t ON r.idOrigen = t.idTerminal
    INNER JOIN Destino d ON r.idDestino = d.idDestino
    ORDER BY r.idRuta DESC;
END
