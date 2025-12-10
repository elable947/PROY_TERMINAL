CREATE OR ALTER PROCEDURE sp_BuscarUsuarioPorDNI
    @dni VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    SELECT idUsuario, nombre_usuario, apPaterno, apMaterno, dni
    FROM Usuario
    WHERE dni = @dni;
END
