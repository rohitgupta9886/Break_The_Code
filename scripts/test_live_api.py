import urllib.request
import json

try:
    print("Testing /health...")
    h = urllib.request.urlopen("http://127.0.0.1:8001/health", timeout=3)
    print("Health response:", h.read().decode())
    
    print("Testing /api/v1/questions...")
    req = urllib.request.urlopen("http://127.0.0.1:8001/api/v1/questions?page_size=1", timeout=5)
    res = json.loads(req.read().decode())
    print("SUCCESS: Connected to live API!")
    print("Total Questions in live API:", res.get("total"))
except Exception as e:
    print("API Error:", e)
