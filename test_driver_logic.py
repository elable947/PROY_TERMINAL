import pyodbc

conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=BD_TERMINAL_MUN;UID=admin_terminal;PWD=terminal1234;TrustServerCertificate=yes;"

def test_logic():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        print("--- TESTING DRIVER LOGIC ---")
        
        # 1. Pick a user (Pasajero) to assign. Let's find one or create one.
        # Actually, let's just pick an existing driver for testing if we can revert it, 
        # but better to assume there's a user id 21 (from user logs) or similar.
        # We'll just query one row from ConductorEmpresa to test on.
        cursor.execute("SELECT TOP 1 idConductorEmpresa, estadoConductorEmpresa FROM ConductorEmpresa WHERE estadoConductorEmpresa IN (0, 1)")
        row = cursor.fetchone()
        
        if not row:
            print("No testable driver found.")
            return

        cid = row[0]
        initial_status = row[1]
        print(f"Testing on DriverID: {cid}, Initial Status: {initial_status}")
        
        # 2. Call Delete SP
        # Get Company ID for this driver
        cursor.execute("SELECT idEmpresaTransporte FROM ConductorEmpresa WHERE idConductorEmpresa = ?", cid)
        eid = cursor.fetchone()[0]
        
        print(f"Calling sp_EliminarConductor for Driver {cid}, Company {eid}...")
        cursor.execute("EXEC sp_EliminarConductor @idConductorEmpresa=?, @idEmpresaTransporte=?", cid, eid)
        conn.commit()
        
        # 3. Check Status
        cursor.execute("SELECT estadoConductorEmpresa FROM ConductorEmpresa WHERE idConductorEmpresa = ?", cid)
        new_status = cursor.fetchone()[0]
        print(f"New Status: {new_status}")
        
        if new_status == 2:
            print("SUCCESS: Status updated to 2 (Deleted).")
        elif new_status == 0:
            print("FAILURE: Status updated to 0 (Inactive) - SP IS OLD VERSION.")
        else:
            print(f"FAILURE: Status is {new_status} (Unknown).")
            
        # 4. Check Listing
        print("Checking List SP...")
        cursor.execute("EXEC sp_ListarConductoresEmpresa @idEmpresaTransporte=?", eid)
        drivers = [r[0] for r in cursor.fetchall()]
        
        if cid in drivers:
            print("FAILURE: Driver still appears in List.")
        else:
            print("SUCCESS: Driver distinct from List.")

        # 5. Restore (Optional, but good manners)
        print("Restoring status...")
        cursor.execute("UPDATE ConductorEmpresa SET estadoConductorEmpresa = ? WHERE idConductorEmpresa = ?", initial_status, cid)
        conn.commit()
        
    except Exception as e:
        print(f"ERROR: {e}")

test_logic()
