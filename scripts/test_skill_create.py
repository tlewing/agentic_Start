import requests
import base64
import json

API_KEY = 'ef5fd367-9a88-42b8-b3cf-c117aeb93d72'
CATALOG_ID = 'b1670146-674a-4730-9e9d-d7d29ba52385'
auth_string = base64.b64encode(f':{API_KEY}'.encode()).decode()
headers = {'Authorization': f'Basic {auth_string}', 'Accept': 'application/json', 'Content-Type': 'application/json'}

# Get categories to find Safety ID
r = requests.get('https://api.365.systems/services/skills/SkillCategories', headers=headers)
cats = r.json()
new_cats = [c for c in cats if c['name'] == 'Safety']
print(f"Found {len(new_cats)} Safety categories")

if new_cats:
    cat_id = new_cats[0]['id']
    print(f'Safety category ID: {cat_id}')

    # Try creating a skill with full error details
    url = f'https://api.365.systems/services/skills/catalog/{CATALOG_ID}/Skills'
    data = {'title': 'Test Skill', 'categoryId': cat_id}
    print(f"\nPOST to: {url}")
    print(f"Data: {json.dumps(data)}")

    r = requests.post(url, headers=headers, json=data)
    print(f'\nStatus: {r.status_code}')
    print(f'Response: {r.text}')

    # Try with different field names
    print("\n--- Trying with 'name' instead of 'title' ---")
    data2 = {'name': 'Test Skill 2', 'categoryId': cat_id}
    r2 = requests.post(url, headers=headers, json=data2)
    print(f'Status: {r2.status_code}')
    print(f'Response: {r2.text}')

    # Check swagger for skill schema
    print("\n--- Checking swagger for Skill schema ---")
    swagger = requests.get('https://api.365.systems/swagger/docs/v1').json()
    if 'definitions' in swagger:
        for key in swagger['definitions']:
            if 'skill' in key.lower():
                print(f"Found definition: {key}")
                print(json.dumps(swagger['definitions'][key], indent=2)[:500])
