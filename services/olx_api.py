# services/olx_api.py
import requests

CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
TOKEN_URL = 'https://api.olx.pt/oauth/token'
OLX_URL = 'https://www.olx.pt/d/anuncio/aluguer-de-autocaravana-casa-mvel-IDIq3qc.html'

def authenticate_olx():
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, data=payload)
    response.raise_for_status()
    return response.json()['access_token']

def check_olx_status(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(OLX_URL, headers=headers)
    return response.status_code

if __name__ == '__main__':
    try:
        access_token = authenticate_olx()
        status_code = check_olx_status(access_token)
        print(f'Status Code: {status_code}')
    except requests.RequestException as e:
        print(f'Error: {e}')