import os
from dotenv import load_dotenv
import requests
import json

# load .env so DEEPSEEK_API_KEY becomes available
load_dotenv()

key = os.getenv('DEEPSEEK_API_KEY')
if not key:
    print('No DEEPSEEK_API_KEY in environment')
    raise SystemExit(1)

url = 'https://openrouter.ai/api/v1/chat/completions'
headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
# Use the same payload shape as app.py
payload = {
    'model': 'deepseek/deepseek-r1:free',
    'messages': [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': 'Test message for diagnostics'}
    ]
}

print('Request payload:')
print(json.dumps(payload, indent=2))

r = requests.post(url, headers=headers, json=payload, timeout=30)
print('\nSTATUS:', r.status_code)
print('HEADERS:', dict(r.headers))
print('BODY:', r.text)

if r.status_code >= 400:
    try:
        print('\nJSON:', r.json())
    except Exception:
        pass
