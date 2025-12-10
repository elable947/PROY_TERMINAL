import pyodbc

conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=BD_TERMINAL_MUN;UID=admin_terminal;PWD=terminal1234;TrustServerCertificate=yes;"

sql_commands = [
    # 1. Alter Table (Handle potential constraint if needed, but simple alteration usually works if no indices depend on it heavily)
    "ALTER TABLE ConductorEmpresa ALTER COLUMN estadoConductorEmpresa INT;",
    
    # 2. Update SP Listar
    """
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
        WHERE ce.idEmpresaTransporte = @idEmpresaTransporte AND ce.estadoConductorEmpresa IN (0, 1);
    END
    """,
    
    # 3. Update SP Eliminar
    """
    CREATE OR ALTER PROCEDURE sp_EliminarConductor
        @idConductorEmpresa INT,
        @idEmpresaTransporte INT
    AS
    BEGIN
        SET NOCOUNT ON;

        -- Verify ownership
        DECLARE @idUsuario INT;
        SELECT @idUsuario = idUsuario 
        FROM ConductorEmpresa 
        WHERE idConductorEmpresa = @idConductorEmpresa AND idEmpresaTransporte = @idEmpresaTransporte;

        IF @idUsuario IS NULL
        BEGIN
            THROW 51000, 'El conductor no pertenece a esta empresa o no existe.', 1;
        END

        BEGIN TRANSACTION;

        -- Set to 2 (Deleted)
        UPDATE ConductorEmpresa
        SET estadoConductorEmpresa = 2
        WHERE idConductorEmpresa = @idConductorEmpresa;

        -- Revert User Role to Pasajero (1)
        UPDATE Usuario
        SET idTipoUsuario = 1
        WHERE idUsuario = @idUsuario;

        COMMIT TRANSACTION;
    END
    """
]

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    for cmd in sql_commands:
        print(f"Executing: {cmd[:50]}...")
        cursor.execute(cmd)
        
    conn.commit()
    print("Migration successful.")
except Exception as e:
    print(f"Error: {e}")
