CREATE OR ALTER PROCEDURE sp_ListarEmpresas
AS
BEGIN
    SET NOCOUNT ON;
    SELECT 
        idEmpresaTransporte, 
        nombreEmpresa, 
        ruc,
        telefonoEmpresa,
        bannerUrl
    FROM EmpresaTransporte
    ORDER BY nombreEmpresa;
END
