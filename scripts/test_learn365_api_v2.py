"""
Test Learn365 API Connection - Version 2
Testing different auth approaches based on documentation
"""
import requests
import json

# Configuration
API_KEY = "ef5fd367-9a88-42b8-b3cf-c117aeb93d72"
TENANT_ID = "6bfd84e47f3f4493a606c23022e1e048"
ENV_ID = "567874efa5e24394939b91bbc5999041"
CATALOG_ID = "b1670146674a47309e9dd7d29ba52385"

print("Testing Learn365 API Connection - v2...")
print(f"API Key: {API_KEY[:8]}...{API_KEY[-4:]}")
print()

# Test 1: Try api.365.systems with Api-Key header
print("Test 1: api.365.systems with Api-Key header")
url = "https://api.365.systems/odata/v2/Catalogs"
headers = {"Api-Key": API_KEY}
try:
    r = requests.get(url, headers=headers, timeout=15)
    print(f"  Status: {r.status_code}")
    print(f"  Headers returned: {dict(r.headers)}")
    if r.status_code == 200:
        print(f"  Response: {r.text[:500]}")
except Exception as e:
    print(f"  Error: {e}")
print()

# Test 2: Try with Authorization Bearer header
print("Test 2: Authorization Bearer header")
url = "https://api.365.systems/odata/v2/Catalogs"
headers = {"Authorization": f"Bearer {API_KEY}"}
try:
    r = requests.get(url, headers=headers, timeout=15)
    print(f"  Status: {r.status_code}")
except Exception as e:
    print(f"  Error: {e}")
print()

# Test 3: Try tenant-specific endpoint
print("Test 3: Tenant-specific endpoint")
url = f"https://api.365.systems/odata/v2/{TENANT_ID}/Catalogs"
headers = {"Api-Key": API_KEY}
try:
    r = requests.get(url, headers=headers, timeout=15)
    print(f"  Status: {r.status_code}")
except Exception as e:
    print(f"  Error: {e}")
print()

# Test 4: Try us-lms regional endpoint with different path
print("Test 4: us-lms with tenant path")
url = f"https://us-lms.365.systems/odata/v2/tenant/{TENANT_ID}/Catalogs"
headers = {"Api-Key": API_KEY}
try:
    r = requests.get(url, headers=headers, timeout=15)
    print(f"  Status: {r.status_code}")
except Exception as e:
    print(f"  Error: {e}")
print()

# Test 5: Check swagger/API documentation endpoint
print("Test 5: Check for swagger docs")
for swagger_url in [
    "https://api.365.systems/swagger",
    "https://api.365.systems/swagger/v1/swagger.json",
    "https://api.365.systems/api-docs",
    "https://us-lms.365.systems/swagger",
]:
    try:
        r = requests.get(swagger_url, timeout=10)
        if r.status_code == 200:
            print(f"  Found: {swagger_url}")
            print(f"  Content-Type: {r.headers.get('Content-Type')}")
            break
    except:
        pass
print()

# Test 6: Try the exact admin URL pattern
print("Test 6: Admin URL pattern")
url = f"https://us-lms.365.systems/api/tenant/{TENANT_ID}/catalogs"
headers = {"Api-Key": API_KEY, "Accept": "application/json"}
try:
    r = requests.get(url, headers=headers, timeout=15)
    print(f"  Status: {r.status_code}")
    if r.status_code != 404:
        print(f"  Response type: {r.headers.get('Content-Type')}")
except Exception as e:
    print(f"  Error: {e}")

print("\nDone.")
