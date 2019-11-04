import requests
url = 'https://datosabiertos.malaga.eu/recursos/transporte/EMT/EMTlineasUbicaciones/lineasyubicaciones.geojson'

def getBuses():
    fileobj = requests.get(url)
    print(fileobj.json)
