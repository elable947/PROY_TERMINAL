import requests
import json
import datetime

BASE_URL = "http://127.0.0.1:5000/api/company"
EMP_ID = 1

def run_test():
    try:
        # 1. Create a dummy driver (Assign existing user to driver)
        # We need a user ID that is a passenger (1). 
        # For reproduction, let's pick a user from the list who is NOT a driver yet?
        # Or better, just pick an existing driver who definitely has trips.
        
        print("1. Find a driver with trips...")
        res = requests.get(f"{BASE_URL}/drivers?idEmpresaTransporte={EMP_ID}")
        drivers = res.json()
        
        target_driver = None
        for d in drivers:
            # Check if they have trips
            t_res = requests.get(f"{BASE_URL}/driver/trips?idUsuario={d['idUsuario']}")
            trips = t_res.json()
            if len(trips) > 0:
                print(f"Found driver {d['idConductorEmpresa']} ({d['nombre_usuario']}) with {len(trips)} trips.")
                target_driver = d
                break
        
        if not target_driver:
            print("No driver with trips found. Cannot reproduce constraint error reliably without creating complex state.")
            # Fallback: Just try to delete the first one and see the error?
            if drivers:
                target_driver = drivers[0]
                print(f"Fallback: Trying to delete driver {target_driver['idConductorEmpresa']} (unknown trip state).")
            else:
                print("No drivers found at all.")
                return

        # 2. Try to Delete
        cid = target_driver['idConductorEmpresa']
        print(f"Attempting to delete Driver {cid}...")
        
        res_del = requests.delete(f"{BASE_URL}/drivers/{cid}?idEmpresaTransporte={EMP_ID}")
        
        print(f"Status Code: {res_del.status_code}")
        print(f"Response Body: {res_del.text}")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    run_test()
