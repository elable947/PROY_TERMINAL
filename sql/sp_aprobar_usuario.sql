CREATE OR ALTER PROCEDURE sp_AprobarUsuario
    @idUsuario INT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Usuario SET esActivo = 1 WHERE idUsuario = @idUsuario;
END
