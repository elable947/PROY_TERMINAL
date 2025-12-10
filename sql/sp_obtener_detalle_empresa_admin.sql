CREATE OR ALTER PROCEDURE sp_ObtenerDetalleEmpresaAdmin
    @idEmpresaTransporte INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        e.idEmpresaTransporte,
        e.nombreEmpresa,
        e.ruc,
        e.razonSocial,
        e.telefonoEmpresa,
        u.nombre_usuario AS usuarioAsignado,
        u.correo AS correoUsuario,
        (SELECT COUNT(*) FROM ConductorEmpresa c WHERE c.idEmpresaTransporte = e.idEmpresaTransporte AND c.estadoConductorEmpresa = 1) as numConductores,
        (SELECT COUNT(*) FROM Vehiculo v WHERE v.idEmpresaTransporte = e.idEmpresaTransporte AND v.estadoVehiculo = 1) as numVehiculos
    FROM EmpresaTransporte e
    LEFT JOIN UsuarioEmpresa ue ON e.idEmpresaTransporte = ue.idEmpresaTransporte
    LEFT JOIN Usuario u ON ue.idUsuario = u.idUsuario
    WHERE e.idEmpresaTransporte = @idEmpresaTransporte;
END
