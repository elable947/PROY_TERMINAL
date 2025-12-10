import pyodbc

conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=BD_TERMINAL_MUN;UID=admin_terminal;PWD=terminal1234;TrustServerCertificate=yes;"

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Usuario'")
    for row in cursor.fetchall():
        print(row[0])
        
    print("-- Sample User --")
    cursor.execute("SELECT TOP 1 nombre_usuario, password FROM Usuario WHERE idTipoUsuario=2") # 2 = Empressa info?
    row = cursor.fetchone()
    if row:
        print(row)
        
except Exception as e:
    print(e)
