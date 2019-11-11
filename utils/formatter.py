def locationJSON(busCode, longitude, latitude):
    json = {
         'busCode': busCode,
         'coordinates': {
            'longitude': longitude,
            'latitude': latitude
         }
      }
    return json

def locationXML(busCode, longitude, latitude):
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<bus>
   <busCode>
      {}
   </busCode>
   <coordinates>
      <longitude>
         {}
      </longitude>
      <latitude>
         {}
      </latitude>
   </coordinates>
</bus>'''.format(busCode, longitude, latitude)
    return xml