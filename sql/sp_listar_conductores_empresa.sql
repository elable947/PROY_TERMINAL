CREATE OR ALTER PROCEDURE sp_ListarConductoresEmpresa
    @idEmpresaTransporte INT
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        ce.idConductorEmpresa,
        u.idUsuario,
        u.nombre_usuario,
        u.apPaterno,
        u.apMaterno,
        u.dni,
        ce.licencia,
        ce.fechaingreso,
        ce.estadoConductorEmpresa
    FROM ConductorEmpresa ce
    INNER JOIN Usuario u ON ce.idUsuario = u.idUsuario
    WHERE ce.idEmpresaTransporte = @idEmpresaTransporte AND ce.estadoConductorEmpresa = 1;
END
