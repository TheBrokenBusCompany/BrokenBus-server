import requests

def uploadImage(image : str):
    url = 'https://api.imgur.com/3/image'
    imageBien = image.replace(' ', '+')
    payload = {'image': imageBien}
    headers = { 'Authorization': 'Client-ID a4383f1dbba5971' }
    response = requests.request('POST', url, headers = headers, data = payload)
    json = response.json()
    '''
    AQUI TENEIS EL LINK PAYASOS
    '''
    link = json['data']['link']
    print(link)