import requests

BASE_URL = "http://127.0.0.1:5000"

def run_tests():
    report = []
    print("=== TRICYCLE RIDE BOOKING API CONSUMER REPORT ===\n")

    # 1. GET all rides
    res = requests.get(f"{BASE_URL}/rides")
    print(f"[GET /rides] Status: {res.status_code} | Count: {len(res.json())} rides")
    report.append(("GET /rides", res.status_code == 200))

    # 2. GET specific ride (ID 3 from spec)
    res = requests.get(f"{BASE_URL}/rides/3")
    print(f"[GET /rides/3] Status: {res.status_code} | Data: {res.json()}")
    report.append(("GET /rides/3", res.status_code == 200))

    # 3. POST new ride
    payload = {"pickup": "7-Eleven Dau", "dropoff": "Bamban Town Plaza"}
    res = requests.post(f"{BASE_URL}/rides", json=payload)
    created = res.json()
    new_id = created.get("ride_id")
    print(f"[POST /rides] Status: {res.status_code} | Created: {created}")
    report.append(("POST /rides", res.status_code == 201))

    # 4. PUT update ride status
    update_payload = {"status": "on the way"}
    res = requests.put(f"{BASE_URL}/rides/{new_id}", json=update_payload)
    print(f"[PUT /rides/{new_id}] Status: {res.status_code} | Updated: {res.json()}")
    report.append((f"PUT /rides/{new_id}", res.status_code == 200))

    # 5. DELETE ride
    res = requests.delete(f"{BASE_URL}/rides/{new_id}")
    print(f"[DELETE /rides/{new_id}] Status: {res.status_code} | Response: {res.json()}")
    report.append((f"DELETE /rides/{new_id}", res.status_code == 200))

    # 6. Error handling check (404 Not Found)
    res = requests.get(f"{BASE_URL}/rides/9999")
    if res.status_code == 404:
        print(f"[ERROR CHECK GET /rides/9999] Handled 404 properly: {res.json().get('error')}")
        report.append(("Error Handling (404)", True))
    else:
        print(f"[ERROR CHECK] Unexpected status: {res.status_code}")
        report.append(("Error Handling (404)", False))

    # Summary Report
    passed = sum(1 for _, ok in report if ok)
    print(f"\n=== SUMMARY: {passed}/{len(report)} endpoints/checks passed ===")

if __name__ == "__main__":
    run_tests()
