CREATE OR ALTER PROCEDURE sp_CancelarReservasExpiradas
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @ExpiredBoletos TABLE (idBoleto INT, idAsiento INT);
    
    -- 1. Identify Expired Reservations (Status 1 = RESERVADO, Older than 5 mins)
    INSERT INTO @ExpiredBoletos (idBoleto, idAsiento)
    SELECT idBoleto, idAsiento
    FROM Boleto
    WHERE idEstadoBoleto = 1 -- RESERVADO
      AND DATEDIFF(minute, fechaCompra, GETDATE()) >= 5;
      
    IF EXISTS (SELECT 1 FROM @ExpiredBoletos)
    BEGIN
        BEGIN TRANSACTION;
        BEGIN TRY
            -- 2. Free Seats
            UPDATE Asiento
            SET disponible = 1
            WHERE idAsiento IN (SELECT idAsiento FROM @ExpiredBoletos);
            
            -- 3. Update Boleto Status to 3 (CANCELADO)
            UPDATE Boleto
            SET idEstadoBoleto = 3 -- CANCELADO
            WHERE idBoleto IN (SELECT idBoleto FROM @ExpiredBoletos);
            
            COMMIT TRANSACTION;
            
            -- Optional: Return count of cancelled items
            SELECT COUNT(*) AS CancelledCount FROM @ExpiredBoletos;
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION;
            THROW;
        END CATCH
    END
    ELSE
    BEGIN
        SELECT 0 AS CancelledCount;
    END
END
