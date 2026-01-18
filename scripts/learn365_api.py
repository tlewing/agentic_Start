"""
Learn365 API Client
Based on swagger docs at api.365.systems/swagger/docs/v1
"""
import requests
import json
import base64

class Learn365Client:
    def __init__(self, api_key, catalog_id):
        self.api_key = api_key
        self.catalog_id = catalog_id
        self.base_url = "https://api.365.systems"
        self.session = requests.Session()

        # Try different auth methods
        self.auth_headers = {
            "Api-Key": api_key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _request(self, method, endpoint, **kwargs):
        """Make authenticated request"""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop('headers', {})
        headers.update(self.auth_headers)

        response = self.session.request(method, url, headers=headers, **kwargs)
        return response

    def test_connection(self):
        """Test API connection with different auth approaches"""
        print("Testing Learn365 API Connection...")
        print()

        # Test 1: Basic Api-Key header
        print("Test 1: Api-Key header on /odata/v2/CourseCatalogs")
        r = self._request("GET", "/odata/v2/CourseCatalogs")
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"  Response: {json.dumps(data, indent=2)[:500]}")
                return True
            except:
                print(f"  Response (non-JSON): {r.text[:200]}")

        # Test 2: Basic Auth with API key as password
        print()
        print("Test 2: Basic Auth (empty user, api key as password)")
        auth_string = base64.b64encode(f":{self.api_key}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth_string}",
            "Accept": "application/json"
        }
        r = requests.get(f"{self.base_url}/odata/v2/CourseCatalogs", headers=headers)
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"  Response: {json.dumps(data, indent=2)[:500]}")
                return True
            except:
                print(f"  Response: {r.text[:200]}")

        # Test 3: Basic Auth with API key as both
        print()
        print("Test 3: Basic Auth (api key as user and password)")
        auth_string = base64.b64encode(f"{self.api_key}:{self.api_key}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth_string}",
            "Accept": "application/json"
        }
        r = requests.get(f"{self.base_url}/odata/v2/CourseCatalogs", headers=headers)
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"  Response: {json.dumps(data, indent=2)[:500]}")
                return True
            except:
                print(f"  Response: {r.text[:200]}")

        # Test 4: X-Api-Key header
        print()
        print("Test 4: X-Api-Key header")
        headers = {
            "X-Api-Key": self.api_key,
            "Accept": "application/json"
        }
        r = requests.get(f"{self.base_url}/odata/v2/CourseCatalogs", headers=headers)
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"  Response: {json.dumps(data, indent=2)[:500]}")
                return True
            except:
                print(f"  Response: {r.text[:200]}")

        return False


if __name__ == "__main__":
    API_KEY = "ef5fd367-9a88-42b8-b3cf-c117aeb93d72"
    CATALOG_ID = "b1670146674a47309e9dd7d29ba52385"

    client = Learn365Client(API_KEY, CATALOG_ID)
    success = client.test_connection()

    if success:
        print("\n=== CONNECTION SUCCESSFUL ===")
    else:
        print("\n=== CONNECTION FAILED ===")
        print("API key may need to be authorized at api.365.systems first")
        print("Or OAuth2 token exchange may be required")
