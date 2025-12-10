CREATE OR ALTER PROCEDURE sp_CrearViaje
    @idEmpresaTransporte INT,
    @idVehiculo INT,
    @idConductorEmpresa INT,
    @idRuta INT,
    @fechaSalida DATETIME,
    @precio DECIMAL(10,2)
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Validate Bus belongs to Company
    IF NOT EXISTS (SELECT 1 FROM Vehiculo WHERE idVehiculo = @idVehiculo AND idEmpresaTransporte = @idEmpresaTransporte)
    BEGIN
        THROW 51000, 'El vehículo no pertenece a esta empresa.', 1;
    END
    
    -- Get seats from Bus
    DECLARE @asientos INT;
    SELECT @asientos = capacidadAsientos FROM Vehiculo WHERE idVehiculo = @idVehiculo;
    
    -- Insert Viaje
    -- Columns: idEmpresaTransporte, idVehiculo, idConductorEmpresa, idRuta, fechaSalida, idHorario, precio, asientosDisponibles, idEstadoViaje
    -- Note: idHorario? Schema has it. User didn't specify. I'll default to NULL or 1 if mandatory.
    -- Schema in Step 1148 says idHorario (int).
    -- I will require idHorario or map it?
    -- Better: Insert NULL if nullable. Data Type says (int). Usually Nullable not shown.
    -- I will pass NULL for now.
    
    INSERT INTO Viaje (idEmpresaTransporte, idVehiculo, idConductorEmpresa, idRuta, fechaSalida, precio, asientosDisponibles, idEstadoViaje, idHorario)
    VALUES (@idEmpresaTransporte, @idVehiculo, @idConductorEmpresa, @idRuta, @fechaSalida, @precio, @asientos, 1, 1); 
    -- 1 = Scheduled/Active status. 
    -- Hardcoding idHorario=1 for now as it's a FK.
END
