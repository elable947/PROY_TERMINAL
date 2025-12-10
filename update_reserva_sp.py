import pyodbc

conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=BD_TERMINAL_MUN;UID=admin_terminal;PWD=terminal1234;TrustServerCertificate=yes;"

def apply_sp():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        with open('sql/sp_reservar_boleto.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
            
        print("Applying sp_reservar_boleto.sql...")
        # Split by GO if exists, though this file looks clean.
        # But wait, it's CREATE OR ALTER, so we can run direct.
        cursor.execute(sql)
        conn.commit()
        print("SUCCESS.")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    apply_sp()
