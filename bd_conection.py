import pyodbc

# conexion a sql server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=BD_TERMINAL_MUN;"
    "UID=admin_terminal;"
    "PWD=terminal1234;"
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()

print("--- Columns of Usuario ---")
cursor.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Usuario'")
rows = cursor.fetchall()
for row in rows:
    print(row)
