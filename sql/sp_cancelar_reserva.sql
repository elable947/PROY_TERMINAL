CREATE OR ALTER PROCEDURE sp_CancelarReserva
    @idBoleto INT,
    @idUsuario INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Verify ticket belongs to user and is in RESERVADO status (1)
    IF EXISTS (
        SELECT 1 FROM Boleto 
        WHERE idBoleto = @idBoleto 
          AND idUsuario = @idUsuario 
          AND idEstadoBoleto = 1 -- RESERVADO
    )
    BEGIN
        BEGIN TRANSACTION;
        TryCatch:
        BEGIN TRY
            -- Update Boleto status to CANCELADO (3)
            UPDATE Boleto 
            SET idEstadoBoleto = 3 
            WHERE idBoleto = @idBoleto;

            -- Get Seat ID
            DECLARE @idAsiento INT;
            SELECT @idAsiento = idAsiento FROM Boleto WHERE idBoleto = @idBoleto;

            -- Release Seat
            UPDATE Asiento
            SET disponible = 1
            WHERE idAsiento = @idAsiento;

            COMMIT TRANSACTION;
            SELECT 1 as success, 'Reserva cancelada exitosamente' as message;
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION;
            SELECT 0 as success, ERROR_MESSAGE() as message;
        END CATCH
    END
    ELSE
    BEGIN
        SELECT 0 as success, 'No se puede cancelar (Boleto no encontrado o no es una reserva activa)' as message;
    END
END
