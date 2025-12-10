CREATE PROCEDURE sp_ListarRedesSociales
    @idEmpresa INT
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT idRedSocial, red, url
    FROM RedSocial
    WHERE idEmpresaTransporte = @idEmpresa;
END
GO
