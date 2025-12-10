CREATE PROCEDURE sp_AgregarRedSocial
    @idEmpresa INT,
    @red VARCHAR(50),
    @url VARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;
    
    INSERT INTO RedSocial (idEmpresaTransporte, red, url)
    VALUES (@idEmpresa, @red, @url);
    
    SELECT SCOPE_IDENTITY() as idRedSocial;
END
GO
