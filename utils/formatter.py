def locationJSON(busCode, longitude, latitude):
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

def locationsJSON(result):
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
      json.append(locationJSON(key, value[0], value[1]))
   return json

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