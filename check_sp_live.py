import pyodbc

conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=BD_TERMINAL_MUN;UID=admin_terminal;PWD=terminal1234;TrustServerCertificate=yes;"

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    print("--- sp_EliminarConductor ---")
    cursor.execute("sp_helptext sp_EliminarConductor")
    for row in cursor.fetchall():
        print(row[0].strip())

    print("\n--- sp_ListarConductoresEmpresa ---")
    cursor.execute("sp_helptext sp_ListarConductoresEmpresa")
    for row in cursor.fetchall():
        print(row[0].strip())
        
except Exception as e:
    print(e)
