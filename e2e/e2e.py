import os
import time
import requests

BACKEND = os.getenv("BACKEND", "http://backend:8000")
FRONTEND = os.getenv("FRONTEND", "http://frontend")


def wait_for(url, timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code < 500:
                return True
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError(f"Service not ready: {url}")


def main():
    wait_for(f"{BACKEND}/docs")

    # Register user
    r = requests.post(f"{BACKEND}/auth/register", json={"username": "u1", "password": "p1"})
    assert r.status_code in (200, 400), r.text  # allow already exists

    # Login user
    r = requests.post(f"{BACKEND}/auth/login", json={"username": "u1", "password": "p1"})
    assert r.ok, r.text
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Menu
    r = requests.get(f"{BACKEND}/user/menu")
    assert r.ok and isinstance(r.json(), list)
    menu = r.json()
    assert menu, "Menu empty"

    # Place order
    first = menu[0]
    r = requests.post(f"{BACKEND}/user/order", headers=headers, json={"items": [{"sku_id": first["id"], "quantity": 2}]})
    assert r.ok, r.text
    order = r.json()

    # Admin login
    r = requests.post(f"{BACKEND}/auth/login", json={"username": "admin", "password": "admin123"})
    assert r.ok, r.text
    admin_token = r.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # Admin view orders
    r = requests.get(f"{BACKEND}/admin/orders", headers=admin_headers)
    assert r.ok and isinstance(r.json(), list)

    # Admin update status
    r = requests.put(f"{BACKEND}/admin/orders/{order['id']}", headers=admin_headers, json={"status": "completed"})
    assert r.ok, r.text

    print("E2E OK")


if __name__ == "__main__":
    main()
