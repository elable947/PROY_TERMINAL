CREATE OR ALTER PROCEDURE sp_ListarUsuariosPendientes
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        u.idUsuario, 
        u.nombre_usuario, 
        u.correo, 
        t.nombreTipoUsuario,
        STRING_AGG(e.nombreEmpresa, ', ') AS empresas_solicitadas
    FROM Usuario u
    JOIN TipoUsuario t ON u.idTipoUsuario = t.idTipoUsuario
    LEFT JOIN UsuarioEmpresa ue ON u.idUsuario = ue.idUsuario
    LEFT JOIN EmpresaTransporte e ON ue.idEmpresaTransporte = e.idEmpresaTransporte
    WHERE u.esActivo = 0
    GROUP BY u.idUsuario, u.nombre_usuario, u.correo, t.nombreTipoUsuario;
END
