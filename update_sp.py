import pyodbc
import os

conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=BD_TERMINAL_MUN;UID=admin_terminal;PWD=terminal1234;TrustServerCertificate=yes;"

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    file_path = r"d:\DATA ING\CICLO IV\Base de Datos I\PROY_TERMINAL\sql\fix_driver_status.sql"
    print(f"Applying {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        sql = f.read()
        try:
            cursor.execute(sql)
            cursor.commit()
            print("SP updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
            
except Exception as e:
    print(f"Connection Error: {e}")
