import urllib.request
import json

req = urllib.request.Request("http://127.0.0.1:8000/api/v1/admin/content/matrix")
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    print("HTTP Status:", resp.status)
    print("Compliance Summary:")
    print(json.dumps(data.get("compliance_summary"), indent=2))
    print(f"Total Technologies: {len(data.get('technologies', []))}")
    for tech in data.get("technologies", []):
        print(f"\n{tech['name']} ({len(tech['sections'])} sections):")
        for sec in tech["sections"]:
            print(f"  [{sec['status']}] {sec['name'][:40]:<40} | L1: {sec['l1_count']}/20 | L2: {sec['l2_count']}/20")
