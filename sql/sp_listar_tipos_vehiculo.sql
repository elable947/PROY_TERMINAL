CREATE OR ALTER PROCEDURE sp_ListarTiposVehiculo
AS
BEGIN
    SET NOCOUNT ON;
    SELECT idTipoVehiculo, nombreTipoVehiculo FROM TipoVehiculo ORDER BY nombreTipoVehiculo;
END
