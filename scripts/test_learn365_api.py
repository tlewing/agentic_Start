"""
Test Learn365 API Connection
"""
import requests
import json

# Configuration
API_KEY = "ef5fd367-9a88-42b8-b3cf-c117aeb93d72"
TENANT_ID = "6bfd84e47f3f4493a606c23022e1e048"
ENV_ID = "567874efa5e24394939b91bbc5999041"
CATALOG_ID = "b1670146674a47309e9dd7d29ba52385"

# Learn365 API base URLs to try
BASE_URLS = [
    "https://us-lms.365.systems",
    "https://api.365.systems",
    f"https://us-lms.365.systems/tenant/{TENANT_ID}",
]

ENDPOINTS = [
    "/odata/v2/Catalogs",
    "/api/v1.0/catalogs",
    "/api/catalogs",
    f"/odata/v2/Catalogs('{CATALOG_ID}')",
    f"/api/v1.0/tenant/{TENANT_ID}/catalogs",
]

headers = {
    "Api-Key": API_KEY,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

print("Testing Learn365 API Connection...")
print(f"API Key: {API_KEY[:8]}...{API_KEY[-4:]}")
print()

for base in BASE_URLS:
    for endpoint in ENDPOINTS:
        url = f"{base}{endpoint}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            status = response.status_code
            content_type = response.headers.get('Content-Type', 'unknown')

            if status == 200 and 'json' in content_type.lower():
                print(f"SUCCESS: {url}")
                print(f"  Status: {status}")
                print(f"  Content-Type: {content_type}")
                data = response.json()
                print(f"  Response keys: {list(data.keys()) if isinstance(data, dict) else 'array'}")
                print()
            elif status == 200:
                print(f"OK (non-JSON): {url}")
                print(f"  Status: {status}, Content-Type: {content_type}")
            elif status in [401, 403]:
                print(f"AUTH ERROR: {url}")
                print(f"  Status: {status} - Check API key permissions")
            elif status == 404:
                pass  # Skip not found
            else:
                print(f"ERROR: {url}")
                print(f"  Status: {status}")

        except requests.exceptions.Timeout:
            print(f"TIMEOUT: {url}")
        except requests.exceptions.ConnectionError:
            print(f"CONNECTION ERROR: {url}")
        except Exception as e:
            print(f"ERROR: {url} - {str(e)[:50]}")

print("\nDone.")
