CREATE OR ALTER PROCEDURE sp_ListarVehiculosEmpresa
    @idEmpresaTransporte INT
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        v.idVehiculo,
        v.placa,
        v.capacidadAsientos,
        v.idTipoVehiculo,
        tv.nombreTipoVehiculo,
        v.estadoVehiculo
    FROM Vehiculo v
    LEFT JOIN TipoVehiculo tv ON v.idTipoVehiculo = tv.idTipoVehiculo
    WHERE v.idEmpresaTransporte = @idEmpresaTransporte AND v.estadoVehiculo = 1;
END
