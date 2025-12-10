CREATE OR ALTER PROCEDURE sp_EditarVehiculo
    @idVehiculo INT,
    @idEmpresaTransporte INT,
    @placa VARCHAR(50),
    @capacidadAsientos INT,
    @idTipoVehiculo INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Verify ownership
    IF NOT EXISTS (SELECT 1 FROM Vehiculo WHERE idVehiculo = @idVehiculo AND idEmpresaTransporte = @idEmpresaTransporte)
    BEGIN
        THROW 51000, 'El vehículo no pertenece a esta empresa o no existe.', 1;
    END

    -- Check uniqueness of placa (excluding current vehicle)
    IF EXISTS (SELECT 1 FROM Vehiculo WHERE placa = @placa AND idVehiculo <> @idVehiculo)
    BEGIN
        THROW 51000, 'La placa ya está registrada en otro vehículo.', 1;
    END

    UPDATE Vehiculo
    SET 
        placa = @placa,
        capacidadAsientos = @capacidadAsientos,
        idTipoVehiculo = @idTipoVehiculo
    WHERE idVehiculo = @idVehiculo;
END
