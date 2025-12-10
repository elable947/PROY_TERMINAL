CREATE OR ALTER PROCEDURE sp_ObtenerAsientosViaje
    @idViaje INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Ensure seats exist
    EXEC sp_GenerarAsientos @idViaje;

    -- Select seats
    -- Logic: 'disponible' column is the source of truth? 
    -- Or check Boletos? usually Boleto issuance updates 'disponible'.
    SELECT 
        idAsiento,
        numeroAsiento,
        disponible
    FROM Asiento
    WHERE idViaje = @idViaje
    ORDER BY numeroAsiento;
END
