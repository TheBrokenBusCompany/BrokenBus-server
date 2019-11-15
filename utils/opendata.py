import requests
ubicacionesJSON = 'https://datosabiertos.malaga.eu/recursos/transporte/EMT/EMTlineasUbicaciones/lineasyubicaciones.geojson'
ubicacionesCSV = 'https://datosabiertos.malaga.eu/recursos/transporte/EMT/EMTlineasUbicaciones/lineasyubicaciones.csv'

def downloadOpenData(url):
    '''
    Downloads data from an url and returns an
    object depending on the file extension of
    the file in the url
    -> Accepts CSV, json or geojson files
    '''
    response = requests.get(url)

    if response.status_code >= 400:
        raise RuntimeError('Error with the request. Error code:' + response.status_code)
    
    if url.endswith('geojson') or url.endswith('json'):
        return response.json()
    elif url.endswith('csv'):
        return response.text
    else:
        raise ValueError('Unknown file format')

def getBusLocations():
    '''
    Returns the latitude and longitude
    for all EMT buses
    '''
    data = downloadOpenData(ubicacionesJSON)
    result = {}

    for entry in data:
        lon, lat = entry['geometry']['coordinates']
        result[entry['codBus']] = (float(lon), float(lat))

    return result


def getBusLocation(code):
    '''
    Returns a bus latitude and longitude
    for a EMT bus given its code.

    Throws ValueError if no bus is found
    '''
    data = downloadOpenData(ubicacionesJSON)

    for entry in data:
        if entry['codBus'] == str(code):
            lon, lat = entry['geometry']['coordinates']
            return float(lon), float(lat)

    raise ValueError('Bus code not found')



if __name__ == '__main__':
    print(getBusLocation('696'))