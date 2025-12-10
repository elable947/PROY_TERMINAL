CREATE OR ALTER PROCEDURE sp_EliminarVehiculo
    @idVehiculo INT,
    @idEmpresaTransporte INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Verify ownership
    IF NOT EXISTS (SELECT 1 FROM Vehiculo WHERE idVehiculo = @idVehiculo AND idEmpresaTransporte = @idEmpresaTransporte)
    BEGIN
        THROW 51000, 'El vehículo no pertenece a esta empresa o no existe.', 1;
    END

    -- Soft Delete
    UPDATE Vehiculo
    SET estadoVehiculo = 0
    WHERE idVehiculo = @idVehiculo;
END
