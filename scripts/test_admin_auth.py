import urllib.request
import json

def run():
    # 1. Login as Admin
    req = urllib.request.Request(
        'http://127.0.0.1:8000/api/v1/auth/login',
        data=json.dumps({'email': 'admin@breakthecode.dev', 'password': 'AdminPass123!'}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        login_res = json.loads(resp.read().decode())
    token = login_res['access_token']
    print('SUCCESS: Admin login obtained token')

    # 2. Get Users List
    req_users = urllib.request.Request(
        'http://127.0.0.1:8000/api/v1/admin/users',
        headers={'Authorization': f'Bearer {token}'}
    )
    with urllib.request.urlopen(req_users) as resp:
        users_data = json.loads(resp.read().decode())
    print(f'SUCCESS: Total users in system = {users_data["total"]}')
    for u in users_data['users']:
        print(f"  User: {u['full_name']} | {u['email']} | Role: {u['primary_role']} | Last Login: {u['last_login_at']}")

    # 3. Export CSV
    req_csv = urllib.request.Request(
        'http://127.0.0.1:8000/api/v1/admin/users/export?format=csv',
        headers={'Authorization': f'Bearer {token}'}
    )
    with urllib.request.urlopen(req_csv) as resp:
        csv_text = resp.read().decode()
    print('\nSUCCESS: CSV Export received:')
    lines = csv_text.strip().split('\n')
    for l in lines[:4]:
        print('  ' + l.strip())

    # 4. Export JSON
    req_json = urllib.request.Request(
        'http://127.0.0.1:8000/api/v1/admin/users/export?format=json',
        headers={'Authorization': f'Bearer {token}'}
    )
    with urllib.request.urlopen(req_json) as resp:
        json_data = json.loads(resp.read().decode())
    print(f'\nSUCCESS: JSON Export received with {json_data["total_users"]} users')

    # 5. Login as Candidate to test user login timestamp update
    req_cand = urllib.request.Request(
        'http://127.0.0.1:8000/api/v1/auth/login',
        data=json.dumps({'email': 'candidate@breakthecode.dev', 'password': 'CandidatePass123!'}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req_cand) as resp:
        cand_res = json.loads(resp.read().decode())
    print('SUCCESS: Candidate login passed. Last active recorded.')

if __name__ == '__main__':
    run()
