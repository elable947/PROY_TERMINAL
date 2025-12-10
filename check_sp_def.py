import pyodbc

conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=BD_TERMINAL_MUN;UID=admin_terminal;PWD=terminal1234;TrustServerCertificate=yes;"

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    cursor.execute("sp_helptext sp_ListarConductoresEmpresa")
    rows = cursor.fetchall()
    print("--- sp_ListarConductoresEmpresa ---")
    for row in rows:
        print(row[0], end='')

    cursor.execute("sp_helptext sp_EliminarConductor")
    rows = cursor.fetchall()
    print("\n--- sp_EliminarConductor ---")
    for row in rows:
        print(row[0], end='')
except Exception as e:
    print(e)
