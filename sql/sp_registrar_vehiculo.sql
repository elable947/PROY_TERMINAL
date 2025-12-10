CREATE OR ALTER PROCEDURE sp_RegistrarVehiculo
    @idEmpresaTransporte INT,
    @placa VARCHAR(50),
    @modelo VARCHAR(100), -- Note: Table schema in Step 1148 shows NO modelo column in Vehiculo. Only idTipoVehiculo?
    -- Table: idVehiculo, idEmpresaTransporte, idTipoVehiculo, placa, capacidadAsientos, estadoVehiculo
    @capacidadAsientos INT,
    @idTipoVehiculo INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Check uniqueness or basic validation
    IF EXISTS (SELECT 1 FROM Vehiculo WHERE placa = @placa)
    BEGIN
        THROW 51000, 'La placa ya está registrada.', 1;
    END

    INSERT INTO Vehiculo (idEmpresaTransporte, placa, capacidadAsientos, idTipoVehiculo, estadoVehiculo)
    VALUES (@idEmpresaTransporte, @placa, @capacidadAsientos, @idTipoVehiculo, 1);
END
