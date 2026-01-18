"""
Fetch and analyze Learn365 Swagger API documentation
"""
import requests
import json

r = requests.get('https://api.365.systems/swagger/docs/v1', timeout=30)
data = r.json()

print('=== Learn365 API Structure ===')
print()
print('Swagger Version:', data.get('swagger', 'N/A'))
print('Info:', data.get('info', {}).get('title', 'N/A'))
print()

print('Security Definitions:')
sec_defs = data.get('securityDefinitions', {})
for name, details in sec_defs.items():
    print(f"  {name}: {details.get('type', 'N/A')}")
    if 'authorizationUrl' in details:
        print(f"    Auth URL: {details['authorizationUrl']}")
    if 'flow' in details:
        print(f"    Flow: {details['flow']}")
print()

print('Relevant Endpoints:')
relevant_keywords = ['course', 'catalog', 'training', 'skill', 'competenc', 'scorm', 'user', 'enroll']
paths = data.get('paths', {})
for path, methods in sorted(paths.items()):
    if any(kw in path.lower() for kw in relevant_keywords):
        method_list = [m.upper() for m in methods.keys() if m != 'parameters']
        print(f"  {', '.join(method_list):12} {path}")

print()
print(f'Total endpoints: {len(paths)}')

# Save full swagger for reference
with open('learn365_swagger.json', 'w') as f:
    json.dump(data, f, indent=2)
print('Full swagger saved to learn365_swagger.json')
