CREATE OR ALTER PROCEDURE sp_ComprarBoleto
    @idUsuario INT,
    @idViaje INT,
    @idAsiento INT,
    @idMetodoPago INT = 1 -- Default Cash/Card
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

        -- Update Asiento
        UPDATE Asiento 
        SET disponible = 0 
        WHERE idAsiento = @idAsiento;

        -- Create Boleto (Estado 1 = Issued)
        DECLARE @idBoleto INT;
        INSERT INTO Boleto (idUsuario, idViaje, idAsiento, idEstadoBoleto, fechaCompra)
        VALUES (@idUsuario, @idViaje, @idAsiento, 1, GETDATE());
        
        SET @idBoleto = SCOPE_IDENTITY();

        -- Create Pago (Mock)
        DECLARE @precio DECIMAL(10,2);
        SELECT @precio = precio FROM Viaje WHERE idViaje = @idViaje;

        INSERT INTO Pago (idBoleto, monto, idMetodoPago, fechaPago, confirmado)
        VALUES (@idBoleto, @precio, @idMetodoPago, GETDATE(), 1);

        -- Update Viaje availability (optional, for performance cache)
        -- UPDATE Viaje SET asientosDisponibles = asientosDisponibles - 1 WHERE idViaje = @idViaje;

        COMMIT TRANSACTION;
        
        SELECT @idBoleto as idBoleto, 'Compra exitosa' as mensaje;
        
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
