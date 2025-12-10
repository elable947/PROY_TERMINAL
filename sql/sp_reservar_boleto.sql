CREATE OR ALTER PROCEDURE sp_ReservarBoleto
    @idUsuario INT,
    @idViaje INT,
    @idAsiento INT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Check availability locked
        IF EXISTS (SELECT 1 FROM Asiento WITH (UPDLOCK) WHERE idAsiento = @idAsiento AND (disponible = 0 OR disponible IS NULL))
        BEGIN
            THROW 51000, 'El asiento ya no está disponible.', 1;
        END

        -- Update Asiento (occupied)
        UPDATE Asiento 
        SET disponible = 0 
        WHERE idAsiento = @idAsiento;

        -- Create Boleto (Assuming 2 = 'Reservado')
        DECLARE @idBoleto INT;
        INSERT INTO Boleto (idUsuario, idViaje, idAsiento, idEstadoBoleto, fechaCompra)
        VALUES (@idUsuario, @idViaje, @idAsiento, 1, GETDATE());
        
        SET @idBoleto = SCOPE_IDENTITY();
        
        -- NO Payment for Reservation
        
        COMMIT TRANSACTION;
        
        SELECT @idBoleto as idBoleto, 'Reserva exitosa' as mensaje;
        
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
