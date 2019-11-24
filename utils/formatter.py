def busJSON(busCode, busData):
   '''
   Converts a bus location into JSON format
   '''

   json = {
        'busCode': busCode,
         'coordinates': {
            'latitude': busData[0],
            'longitude': busData[1]
         },
         'codLine': busData[2],
         'direction': busData[3],
         'lastUpdate': busData[4]
      }
   return json

def busesJSON(busesData):
   '''
   Converts a list of bus locations into JSON format
   Expects a dict in the following format:
   {
      busCode: (lat,long,codLine,direction,lastUpdate),
      busCode2: (lat, long,codLine,direction,lastUpdate),
      ...
   }
   '''
   json = []
   for key, value in busesData.items():
      json.append(busJSON(key, value))
   return json

def busGeoJSON(busCode, busData):
   '''
   Converts a bus location into GeoJSON format
   '''
   json = {
         'type': 'Feature',
         'geometry': {
            'type': 'Point',
            'coordinates': [
               busData[0],
               busData[1]
            ]
         },
         'properties':{
            'busCode': busCode,
            'codLine': busData[2],
            'direction': busData[3],
            'lastUpdate': busData[4]
         }
   }
   return json

def busesGeoJSON(busesData):
   '''
   Converts a list of bus locations into GeoJSON format
   Expects a dict in the following format:
   {
      busCode: (lat,long,codLine,direction,lastUpdate),
      busCode2: (lat, long,codLine,direction,lastUpdate),
      ...
   }
   '''
   json = []
   for key, value in busesData.items():
      json.append(busGeoJSON(key, value))

   geojson = {
      "type": "FeatureCollection",
      "features": json
   }
   
   return geojson


def busXML(busCode, busData, header=True):
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
\t\t<latitude>
\t\t\t{}
\t\t</latitude>
\t\t<longitude>
\t\t\t{}
\t\t</longitude>
\t</coordinates>
\t<routeCode>
\t\t{}
\t</routeCode>
\t<direction>
\t\t{}
\t</direction>
\t<lastUpdate>
\t\t{}
\t</lastUpdate>
</bus>'''.format(busCode, busData[0], busData[1], busData[2], busData[3], busData[4])
   return xml

def busesXML(busesData):
   '''
   Converts a list of bus locations into XML format
   Expects a dict in the following format:
   {
      busCode: (lat,long,codLine,direction,lastUpdate),
      busCode2: (lat, long,codLine,direction,lastUpdate),
      ...
   }
   '''
   xml = '<?xml version="1.0" encoding="UTF-8"?>\n<buses>\n'

   for key, value in busesData.items():
      xml = xml + busXML(key, value, header=False) + '\n'
   xml = xml + '</buses>'
   return xml

def stopJSON(code, stopData):
	'''
	Converts a stop location into JSON format
	'''
	json = {
		'stopCode': code,
		'stopName': stopData[0],
		'coordinates': {
         'latitude': stopData[1],
			'longitude': stopData[2]
		}
	}
	return json

def stopsJSON(stopsData):
   '''
   Converts a list of stops locations into JSON format
   Expects a dict in the following format:
   {
      stopCode: (name, lat,long),
      stopCode2: (name, lat, long),
      ...
   }
   '''
   json = []
   for key, value in stopsData.items():
      json.append(stopJSON(key, value))
   return json

def stopGeoJSON(code, stopData):
	'''
	Converts a stop location into GeoJSON format
	'''
	json = {
      'type': 'Feature',
      'geometry': {
         'type': 'Point',
         'coordinates': [
            stopData[1],
            stopData[2]
         ]
      },
      'properties':{
         'stopCode': code,
         'stopName': stopData[0]
      }
	}
	return json

def stopsGeoJSON(result):
   '''
   Converts a list of stops locations into GeoJSON format
   Expects a dict in the following format:
   {
      stopCode: (name, lat,long),
      stopCode2: (name, lat,long),
      ...
   }
   '''
   json = []
   for key, value in result.items():
      json.append(stopGeoJSON(key, value))

   geojson = {
      "type": "FeatureCollection",
      "features": json
   }

   return geojson

def stopXML(code, stopData, header=True):
   '''
   Converts a stop location into XML format
   '''
   if header:
      xml = '<?xml version="1.0" encoding="UTF-8"?>'
   else:
      xml = ''

   xml = xml + '''<busStop>
\t<code>
\t\t{}
\t</code>
\t<name>
\t\t{}
\t</name>
\t<coordinates>
\t\t<latitude>
\t\t\t{}
\t\t</latitude>
\t\t<longitude>
\t\t\t{}
\t\t</longitude>
\t</coordinates>
</busStop>'''.format(code, stopData[0], stopData[1], stopData[2])
   return xml

def stopsXML(stopsData):
   '''
   Converts a list of stops locations into XML format
   Expects a dict in the following format:
   {
      stopCode: (name, lat,long),
      stopCode2: (name, lat,long),
      ...
   }
   '''
   xml = '<?xml version="1.0" encoding="UTF-8"?>\n<busStops>\n'

   for key, value in stopsData.items():
      xml = xml + stopXML(key, value, header=False) + '\n'
   xml = xml + '</busStops>'
   return xml

def commentJSON(id, commentData):
   '''
	Converts a comment data into JSON format
	'''
   json = {
      'id': id,
      'userId': commentData[0],
      'EMTCode': commentData[1],
      'body': commentData[2],
      'imageURL': commentData[3]
   }

   return json

def commentsJSON(commentsData):
   '''
   Converts a list of comments into JSON format
   Expects a list in the following format:
   [
      (commentId, userId, EMTCode, body, imageURL),
      (commentId2, userId, EMTCode, body, imageURL),
      ...
   ]
   '''
   json = []

   for comment in commentsData:
      json.append(commentJSON(comment[0],comment[1:]))
   
   return json

def commentXML(id, commentData, header=True):
   '''
   Converts a comment into XML format
   '''
   if header:
      xml = '<?xml version="1.0" encoding="UTF-8"?>'
   else:
      xml = ''

   xml = xml + '''<comment>
\t<id>
\t\t{}
\t</id>
\t<userId>
\t\t{}
\t</userId>
\t<EMTCode>
\t\t{}
\t</EMTCode>
\t<body>
\t\t{}
\t</body>
\t<imageURL>
\t\t{}
\t</imageURL>
</comment>'''.format(id, commentData[0], commentData[1], commentData[2], commentData[3])
   return xml

def commentsXML(commentsData):
   '''
   Converts a list of comments into XML format
   Expects a list in the following format:
   [
      (commentId, userId, EMTCode, body, imageURL),
      (commentId2, userId, EMTCode, body, imageURL),
      ...
   ]
   '''
   xml = '<?xml version="1.0" encoding="UTF-8"?>\n<comments>\n'

   for value in commentsData:
      xml = xml + json.append(commentXML(value[0], value[1:], header=False)) + '\n'
   xml = xml + '</comments>'
   return xml

def userJSON(id, userData):
   '''
	Converts a user data into JSON format
   '''
   json = {
      'id': id, 
      'email': userData[0],
      'username': userData[1]
      }
   return json

def usersJSON(usersData):
   '''
   Converts a list of users into JSON format
   Expects a list in the following format:
   [
      (user1, email,username),
      (user2, email,username),
      ...
   ]
      '''
   json = []
   for value in usersData:
      json.append(userJSON(value[0], value[1:]))
   return json

def userXML(id, userData, header=True):
   '''
   Converts a user into XML format
   '''
   if header:
      xml = '<?xml version="1.0" encoding="UTF-8"?>'
   else:
      xml = ''

   xml = xml + '''<user>
\t<id>
\t\t{}
\t</id>
\t<email>
\t\t{}
\t</email>
\t<username>
\t\t{}
\t</username>
</user>'''.format(id, userData[0], userData[1])
   return xml

def usersXML(usersData):
   '''
   Converts a list of users into XML format
   Expects a list in the following format:
   [
      (user1, email,username),
      (user2, email,username),
      ...
   ]
   '''
   xml = '<?xml version="1.0" encoding="UTF-8"?>\n<users>\n'

   for value in usersData:
      xml = xml + json.append(userXML(value[0], value[1:], header=False)) + '\n'
   xml = xml + '</users>'
   return xml