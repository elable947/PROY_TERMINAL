import os
import urllib.parse

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'u-will-never-guess'
    
    # Database connection parameters from bd_conection.py
    # DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=BD_TERMINAL_MUN;UID=admin_terminal;PWD=terminal1234;TrustServerCertificate=yes;
    
    # Database connection parameters
    # Intentamos detectar el driver o usar uno por defecto robusto
    # Nota: Para SQL Server en Docker o Azure, Driver 17 o 18 son comunes.
    
    # Definimos los parametros base
    params_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=BD_TERMINAL_MUN;"
        "UID=admin_terminal;"
        "PWD=terminal1234;"
        "TrustServerCertificate=yes;"
    )
    
    params = urllib.parse.quote_plus(params_str)
    
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
