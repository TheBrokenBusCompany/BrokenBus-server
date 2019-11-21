
def busJSON(busCode, latitude, longitude):
   '''
   Converts a bus location into JSON format
   '''
   json = {
        'busCode': busCode,
         'coordinates': {
            'latitude': latitude,
            'longitude': longitude
         }
      }
   return json

def busesJSON(result):
   '''
   Converts a list of bus locations into JSON format
   Expects a dict in the following format:
   {
      busCode: (lat,long),
      busCode2: (lat, long),
      ...
   }
   '''
   json = []
   for key, value in result.items():
      json.append(busJSON(key, value[0], value[1]))
   return json

def busGeoJSON(busCode, latitude, longitude):
   '''
   Converts a bus location into GeoJSON format
   '''
   json = {
         'type': 'Feature',
         'geometry': {
            'type': 'Point',
            'coordinates': [
               latitude,
               longitude
            ]
         },
         'properties':{
            'busCode': busCode
         }
   }
   return json

def busesGeoJSON(result):
   '''
   Converts a list of bus locations into GeoJSON format
   Expects a dict in the following format:
   {
      busCode: (lat,long),
      busCode2: (lat, long),
      ...
   }
   '''
   json = []
   for key, value in result.items():
      json.append(busGeoJSON(key, value[0], value[1]))

   geojson = {
      "type": "FeatureCollection",
      "features": json
   }
   
   return geojson


def busXML(busCode, longitude, latitude, header=True):
   '''
   Converts a bus location into XML format
   '''
   if header:
      xml = '<?xml version="1.0" encoding="UTF-8"?>'
   else:
      xml = ''

   xml = xml + '''<bus>
\t<busCode>
\t\t{}
\t</busCode>
\t<coordinates>
\t\t<longitude>
\t\t\t{}
\t\t</longitude>
\t\t<latitude>
\t\t\t{}
\t\t</latitude>
\t</coordinates>
</bus>'''.format(busCode, longitude, latitude)
   return xml

def busesXML(result):
   '''
   Converts a list of bus locations into XML format
   Expects a dict in the following format:
   {
      busCode: (lat,long),
      busCode2: (lat, long),
      ...
   }
   '''
   xml = '<?xml version="1.0" encoding="UTF-8"?>\n<buses>\n'

   for key, value in result.items():
      xml = xml + busXML(key, value[0], value[1], header=False) + '\n'
   xml = xml + '</buses>'
   return xml

def stopJSON(code, name, latitude, longitude):
	'''
	Converts a stop location into JSON format
	'''
	json = {
		'stopCode': code,
		'stopName': name,
		'coordinates': {
         'latitude': latitude,
			'longitude': longitude
		}
	}
	return json

def stopsJSON(result):
   '''
   Converts a list of bus locations into JSON format
   Expects a dict in the following format:
   {
      busCode: (name, lat,long),
      busCode2: (name, lat, long),
      ...
   }
   '''
   json = []
   for key, value in result.items():
      json.append(stopJSON(key, value[0], value[1], value[2]))
   return json

def stopGeoJSON(code, name, latitude, longitude):
	'''
	Converts a stop location into GeoJSON format
	'''
	json = {
      'type': 'Feature',
      'geometry': {
         'type': 'Point',
         'coordinates': [
            latitude,
            longitude
         ]
      },
      'properties':{
         'stopCode': code,
         'stopName': name
      }
	}
	return json

def stopsGeoJSON(result):
   '''
   Converts a list of bus locations into GeoJSON format
   Expects a dict in the following format:
   {
      busCode: (lat,long),
      busCode2: (lat, long),
      ...
   }
   '''
   json = []
   for key, value in result.items():
      json.append(stopGeoJSON(key, value[0], value[1], value[2]))

   geojson = {
      "type": "FeatureCollection",
      "features": json
   }

   return geojson

def commentJSON(id, usuario_id, codigoEMT, texto, imagen):
   json = {
      'id': id,
      'usuario_id': usuario_id,
      'codigoEMT': codigoEMT,
      'texto': texto,
      'imagen': imagen
   }

   return json

def commentsJSON(result):
   json = []

   for comment in result:
      json.append(commentJSON(comment[0],comment[1],comment[2],comment[3],comment[4]))
   
   return json