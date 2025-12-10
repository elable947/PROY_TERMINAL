import pyodbc

conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=BD_TERMINAL_MUN;UID=admin_terminal;PWD=terminal1234;TrustServerCertificate=yes;"

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DATA_TYPE 
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'ConductorEmpresa' AND COLUMN_NAME = 'estadoConductorEmpresa'
    """)
    
    row = cursor.fetchone()
    if row:
        print(f"Type: {row[0]}")
    else:
        print("Column not found")
        
except Exception as e:
    print(e)
