import requests
import json

with open ('secrets.json') as file:
    data = json.load(file)
    clientId = data['imgurClientId']

def uploadImage(image : str):
    '''
    Receives a base64 encoding of a image, posts it to imgur
    and returns a link to it.
    '''
    url = 'https://api.imgur.com/3/image'
    # Fixing base64 encoding after HTTP request
    fixedImage = image.replace(' ', '+')
    payload = {'image': fixedImage}
    headers = { 'Authorization': 'Client-ID ' + clientId }
    response = requests.request('POST', url, headers = headers, data = payload)
    json = response.json()
    if response.status_code != 200:
        return None
    link = json['data']['link']
    return link