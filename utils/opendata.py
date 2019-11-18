import requests
ubicacionesJSON = 'https://datosabiertos.malaga.eu/recursos/transporte/EMT/EMTlineasUbicaciones/lineasyubicaciones.geojson'
ubicacionesCSV = 'https://datosabiertos.malaga.eu/recursos/transporte/EMT/EMTlineasUbicaciones/lineasyubicaciones.csv'
paradasJSON = 'https://datosabiertos.malaga.eu/recursos/transporte/EMT/EMTLineasYParadas/lineasyparadas.geojson'

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

def getAllStopsLocation():
	'''
    Returns the latitude and longitude
    for all EMT stops
    '''
	data = downloadOpenData(paradasJSON)
	result = {}
	
	for linea in data:
		for parada in linea['paradas']:
			p = parada['parada']
			codigo = p['codParada']
			nombre = p['nombreParada']
			lon = p['longitud']
			lat = p['latitud']
			result[codigo] = (nombre, lon, lat)
			
	return result

def getOneStopLocation(code):
	'''
	Returns a stop latitude, longitude
	and name for a EMT stop given its code.

	Throws ValueError if no stop is found
	'''
	data = downloadOpenData(paradasJSON)
	
	for linea in data:
		for parada in linea['paradas']:
			p = parada['parada']
			if str(p['codParada']) == str(code):
				nombre = p['nombreParada']
				lon = p['longitud']
				lat = p['latitud']
				return (nombre, lon, lat)
	
	raise ValueError('Stop code not found')
	
def getBusesInRoute(routeCode):
	'''
	Returns all the buses in a route.

	Throws ValueError if no route is found
	'''
	data = downloadOpenData(ubicacionesJSON)
	result = {}
	
	for entry in data:
		codLinea = entry['codLinea']
		if float(routeCode) == float(codLinea) :
			codBus = entry['codBus']
			lon, lat = entry['geometry']['coordinates']
			result[codBus] = (lon, lat)
	
	if result:		
		return result
	else:
		raise ValueError('Route code not found')

if __name__ == '__main__':
    print(getBusesInRoute(1.0))