CREATE OR ALTER PROCEDURE sp_CrearEmpresa
    @nombreEmpresa VARCHAR(255),
    @razonSocial VARCHAR(255) = NULL,
    @ruc VARCHAR(20),
    @telefonoEmpresa VARCHAR(50) = NULL,
    @NewId INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    IF EXISTS (SELECT 1 FROM EmpresaTransporte WHERE ruc = @ruc)
    BEGIN
        THROW 51000, 'El RUC ya está registrado.', 1;
    END

    INSERT INTO EmpresaTransporte (nombreEmpresa, razonSocial, ruc, telefonoEmpresa)
    VALUES (@nombreEmpresa, ISNULL(@razonSocial, @nombreEmpresa), @ruc, @telefonoEmpresa);
    
    SET @NewId = SCOPE_IDENTITY();
END
