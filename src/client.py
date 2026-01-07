import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'https://recipe-api.com'

class RecipeApiError(Exception):
    def __init__(self, message, status, code=None):
        super().__init__(message)
        self.status = status
        self.code = code

def get_api_key():
    key = os.getenv('RECIPE_API_KEY')

    if not key:
        print('\n[X] Missing API key!\n')
        print('To fix this:')
        print('  1. Copy .env.example to .env')
        print('  2. Add your API key from https://recipe-api.com\n')
        sys.exit(1)

    if not key.startswith('rapi_'):
        print('\n[X] Invalid API key format!\n')
        print('API keys should start with "rapi_"')
        print('Get your key from https://recipe-api.com\n')
        sys.exit(1)

    return key

def api_request(endpoint, params=None):
    api_key = get_api_key()
    
    # Construct full URL
    url = f"{BASE_URL}{endpoint}"
    
    headers = {
        'X-API-Key': api_key,
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        
        if not response.ok:
            handle_error_response(response)
            
        return response.json()
        
    except requests.RequestException as e:
        # Check if it was handled by handle_error_response (raised RecipeApiError)
        # But requests raises RequestException on connection errors, not on 4xx/5xx responses usually unless raise_for_status is called
        # Our handle_error_response calls sys.exit or raises RecipeApiError.
        
        print('\n[X] Network error!\n')
        print('Could not connect to the API. Please check:')
        print('  - Your internet connection')
        print('  - The API status at https://recipe-api.com\n')
        sys.exit(1)

def handle_error_response(response):
    status = response.status_code
    
    if status == 401:
        print('\n[X] Authentication failed!\n')
        print('Your API key was rejected. Please check:')
        print('  - The key is copied correctly (no extra spaces)')
        print('  - The key is active in your dashboard\n')
        sys.exit(1)
        
    elif status == 403:
        print('\n[X] Access denied!\n')
        print('Your account may not have access to this endpoint.')
        print('Check your plan limits at https://recipe-api.com\n')
        sys.exit(1)
        
    elif status == 404:
        raise RecipeApiError('Resource not found', 404, 'NOT_FOUND')
        
    elif status == 429:
        print('\n[X] Rate limit exceeded!\n')
        print('You have exceeded your API limits.')
        print('Check your remaining quota in the dashboard.\n')
        sys.exit(1)
        
    else:
        print(f'\n[X] API error ({status})!\n')
        print('Response:', response.text[:500])
        sys.exit(1)
