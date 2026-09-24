import urllib.request
import json

# 1. Login as admin
login_req = urllib.request.Request(
    "http://127.0.0.1:8000/api/v1/auth/login",
    data=json.dumps({"email": "admin@breakthecode.dev", "password": "AdminPass123!"}).encode(),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(login_req) as resp:
    token_data = json.loads(resp.read().decode())
    token = token_data["access_token"]
    print("Admin logged in successfully.")

# 2. List Users
list_req = urllib.request.Request(
    "http://127.0.0.1:8000/api/v1/admin/users",
    headers={"Authorization": f"Bearer {token}"}
)
with urllib.request.urlopen(list_req) as resp:
    users_data = json.loads(resp.read().decode())
    print(f"Total Users Found: {users_data['total']}")
    for u in users_data["users"]:
        print(f"  * {u['email']} | {u['full_name']} | Role: {u['primary_role']} | Last Login: {u['last_login_at']}")

# 3. Test Export (CSV)
export_req = urllib.request.Request(
    "http://127.0.0.1:8000/api/v1/admin/users/export?format=csv",
    headers={"Authorization": f"Bearer {token}"}
)
with urllib.request.urlopen(export_req) as resp:
    csv_text = resp.read().decode()
    print("\nCSV Export Sample:")
    print("\n".join(csv_text.strip().split("\n")[:3]))
