CREATE OR ALTER PROCEDURE sp_ValidarLogin
    @Usuario VARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        u.idUsuario,
        u.password,
        u.idTipoUsuario,
        u.nombre_usuario,
        u.esActivo,
        u.apPaterno,
        u.apMaterno,
        u.correo,
        u.telefono,
        u.edad,
        u.dni,
        u.idPais,
        t.nombreTipoUsuario,
        -- Get Company ID for Enterprise Users (2) or Drivers (4)
        COALESCE(ue.idEmpresaTransporte, ce.idEmpresaTransporte, NULL) as idEmpresaTransporte,
        -- Get Company Name for display
        COALESCE(e1.nombreEmpresa, e2.nombreEmpresa, NULL) as nombreEmpresa
    FROM Usuario u
    LEFT JOIN TipoUsuario t ON u.idTipoUsuario = t.idTipoUsuario
    LEFT JOIN UsuarioEmpresa ue ON u.idUsuario = ue.idUsuario
    LEFT JOIN ConductorEmpresa ce ON u.idUsuario = ce.idUsuario
    LEFT JOIN EmpresaTransporte e1 ON ue.idEmpresaTransporte = e1.idEmpresaTransporte
    LEFT JOIN EmpresaTransporte e2 ON ce.idEmpresaTransporte = e2.idEmpresaTransporte
    WHERE u.nombre_usuario = @Usuario;
END
