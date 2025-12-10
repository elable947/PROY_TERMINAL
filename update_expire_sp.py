import pyodbc

conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=BD_TERMINAL_MUN;UID=admin_terminal;PWD=terminal1234;TrustServerCertificate=yes;"

def apply_sp():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        with open('sql/sp_cancelar_reservas_expiradas.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
            
        print("Applying sp_cancelar_reservas_expiradas.sql...")
        cursor.execute(sql)
        conn.commit()
        print("SUCCESS.")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    apply_sp()
