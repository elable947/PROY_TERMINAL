CREATE PROCEDURE sp_EliminarRedSocial
    @idRedSocial INT,
    @idEmpresa INT -- Security check
AS
BEGIN
    SET NOCOUNT ON;
    
    DELETE FROM RedSocial
    WHERE idRedSocial = @idRedSocial AND idEmpresaTransporte = @idEmpresa;
END
GO
