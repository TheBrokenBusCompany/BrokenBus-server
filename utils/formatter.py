from flask import Response, json

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

def busesGeoJSON(result):
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
      json.append(busGeoJSON(key, value[0], value[1]))
   return json

def busJSON(busCode, longitude, latitude):
   '''
   Converts a bus location into JSON format
   '''
   json = {
        'busCode': busCode,
         'coordinates': {
            'longitude': longitude,
            'latitude': latitude
         }
      }
   return json

def busGeoJSON(busCode, longitude, latitude):
   '''
   Converts a bus location into GepJSON format
   '''
   json = {
         'type': 'Feature',
         'geometry': {
            'type': 'Point',
            'coordinates': [
               longitude,
               latitude
            ]
         },
         'properties':{
            'busCode': busCode
         }
   }
   return json

def stopJSON(code, name, longitude, latitude):
	'''
	Converts a stop location into JSON format
	'''
	json = {
		'stopCode': code,
		'stopName': name,
		'coordinates': {
			'longitude': longitude,
			'latitude': latitude
		}
	}
	return json

def stopsJSON(result):
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
		json.append(stopJSON(key, value[0], value[1], value[2]))
	return json

def error(code, message):
   response = {
      code : message
   }
   return Response(json.dumps(response), mimetype='application/json', status=404)

def locationXML(busCode, longitude, latitude, header=True):
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

def locationsXML(result):
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
      xml = xml + locationXML(key, value[0], value[1], header=False) + '\n'
   xml = xml + '</buses>'
   return xml