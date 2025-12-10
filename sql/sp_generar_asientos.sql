CREATE OR ALTER PROCEDURE sp_GenerarAsientos
    @idViaje INT
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @capacidad INT;
    SELECT @capacidad = v.capacidadAsientos 
    FROM Viaje t
    INNER JOIN Vehiculo v ON t.idVehiculo = v.idVehiculo
    WHERE t.idViaje = @idViaje;

    IF @capacidad IS NULL RETURN;

    DECLARE @existing INT;
    SELECT @existing = COUNT(*) FROM Asiento WHERE idViaje = @idViaje;

    -- If we have enough seats, stop.
    IF @existing >= @capacidad RETURN;
    
    -- Continue loop from next number
    DECLARE @i INT = @existing + 1;
    WHILE @i <= @capacidad
    BEGIN
        INSERT INTO Asiento (idViaje, numeroAsiento, disponible)
        VALUES (@idViaje, @i, 1);
        SET @i = @i + 1;
    END
END
