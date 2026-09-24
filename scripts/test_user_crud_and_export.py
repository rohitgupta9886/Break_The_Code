import urllib.request
import json

BASE = "http://127.0.0.1:8000/api/v1"

def api_call(path, method="GET", data=None, token=None):
    url = f"{BASE}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=10) as resp:
        resp_data = resp.read().decode("utf-8")
        media_type = resp.headers.get("Content-Type", "")
        if "application/json" in media_type:
            return json.loads(resp_data)
        return resp_data

def main():
    print("=== TESTING COMPLETE ADMIN AUTH, CRUD, AND EXPORT ===")
    
    # 1. Admin Login
    login_res = api_call("/auth/login", method="POST", data={
        "email": "admin@breakthecode.dev",
        "password": "AdminPass123!"
    })
    token = login_res["access_token"]
    print("[PASS] 1. Admin logged in successfully. Token acquired.")

    # 2. View all users with login details
    users_res = api_call("/admin/users", token=token)
    print(f"[PASS] 2. Fetched users list. Total users: {users_res['total']}")
    for u in users_res["users"]:
        print(f"       -> {u['full_name']} | {u['email']} | Role: {u['primary_role']} | Last Login: {u['last_login_at']}")

    # 3. Create a new user (CRUD: Create)
    test_email = "jane.dev@fortune500.com"
    create_res = api_call("/admin/users", method="POST", data={
        "full_name": "Jane Developer",
        "email": test_email,
        "password": "SecurePassword123!",
        "role": "USER",
        "is_active": True
    }, token=token)
    new_user_id = create_res["user_id"]
    print(f"[PASS] 3. Created new user: {test_email} (ID: {new_user_id})")

    # 4. Read created user (CRUD: Read)
    detail_res = api_call(f"/admin/users/{new_user_id}", token=token)
    assert detail_res["user"]["email"] == test_email
    print(f"[PASS] 4. Verified user details read: {detail_res['user']['full_name']} ({detail_res['user']['email']})")

    # 5. Update user (CRUD: Update - modify name & role)
    update_res = api_call(f"/admin/users/{new_user_id}", method="PUT", data={
        "full_name": "Jane Senior Developer",
        "role": "ADMIN",
        "is_active": True
    }, token=token)
    print(f"[PASS] 5. Updated user: {update_res['message']}")

    # Verify update
    detail_after = api_call(f"/admin/users/{new_user_id}", token=token)
    assert detail_after["user"]["full_name"] == "Jane Senior Developer"
    assert "ADMIN" in detail_after["user"]["roles"]
    print(f"[PASS] 5b. Verified user updated fields: Full Name={detail_after['user']['full_name']}, Roles={detail_after['user']['roles']}")

    # 6. Export Users to CSV
    csv_res = api_call("/admin/users/export?format=csv", token=token)
    csv_lines = csv_res.strip().split("\n")
    print(f"[PASS] 6. Exported CSV successfully ({len(csv_lines)} lines). Sample rows:")
    for row in csv_lines[:3]:
        print(f"       {row.strip()}")

    # 7. Export Users to JSON
    json_res = api_call("/admin/users/export?format=json", token=token)
    print(f"[PASS] 7. Exported JSON successfully. Total records exported: {json_res['total_users']}")

    # 8. Delete user (CRUD: Delete)
    del_res = api_call(f"/admin/users/{new_user_id}", method="DELETE", token=token)
    print(f"[PASS] 8. Deleted test user: {del_res['message']}")

    # 9. Verify user deleted
    users_final = api_call("/admin/users", token=token)
    assert not any(u["id"] == new_user_id for u in users_final["users"])
    print(f"[PASS] 9. Confirmed user {test_email} removed from database. Total remaining: {users_final['total']}")

    print("\nALL VERIFICATIONS PASSED 100%!")

if __name__ == "__main__":
    main()
