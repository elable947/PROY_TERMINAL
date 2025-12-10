import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/company"
EMP_ID = 1

def run_test():
    try:
        # 1. List Drivers
        print("1. Listing Drivers...")
        res = requests.get(f"{BASE_URL}/drivers?idEmpresaTransporte={EMP_ID}")
        if res.status_code != 200:
            print(f"FAILED to list: {res.text}")
            return
        
        drivers = res.json()
        print(f"Found {len(drivers)} drivers.")
        if not drivers:
            print("No drivers found. Cannot test delete.")
            return

        # Pick one (preferably one we can sacrifice or restore, but for now we pick the last one)
        target = drivers[-1]
        cid = target['idConductorEmpresa']
        print(f"Target Driver: {cid} ({target.get('nombre_usuario', 'Unknown')}) Status: {target.get('estadoConductorEmpresa')}")

        # 2. Delete Driver
        print(f"2. Deleting Driver {cid}...")
        # Note: The service uses DELETE /drivers/{id}?idEmpresaTransporte={eid}
        res_del = requests.delete(f"{BASE_URL}/drivers/{cid}?idEmpresaTransporte={EMP_ID}")
        
        if res_del.status_code == 200:
            print("Delete request successful.")
        else:
            print(f"Delete request FAILED: {res_del.text}")
            return

        # 3. Verify List Update
        print("3. Verifying List Update...")
        res_after = requests.get(f"{BASE_URL}/drivers?idEmpresaTransporte={EMP_ID}")
        drivers_after = res_after.json()
        
        found = any(d['idConductorEmpresa'] == cid for d in drivers_after)
        
        if found:
            print("FAILURE: Driver STILL present in list after API delete.")
        else:
            print("SUCCESS: Driver removed from list via API.")

        # Optional: Restore (if you checked the type earlier, you could direct SQL restore, but via API we can't 'undelete')

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    run_test()
