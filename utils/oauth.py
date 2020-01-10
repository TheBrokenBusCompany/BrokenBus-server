from google.oauth2 import id_token
from google.auth.transport import requests
import json

with open ('secrets.json') as file:
    data = json.load(file)
    clientId = data['OAuthClientId']


def verifyToken(token_id):
    '''
    Verify id token and returns the decoded needed information
    Docs: https://developers.google.com/identity/sign-in/web/backend-auth
    '''
    # Specify the CLIENT_ID of the app that accesses the backend:
    idinfo = id_token.verify_oauth2_token(token_id, requests.Request(), clientId)

    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')

    # ID token is valid. Get the user's Google Account ID from the decoded token.

    return {
        'userid': idinfo['sub'],
        'name': idinfo['name'],
        'email': idinfo['email'],
        'image': idinfo['picture']
    }
