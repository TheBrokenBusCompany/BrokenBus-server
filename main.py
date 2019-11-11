from flask import Flask, request, Response
import utils.opendata as opendata
import utils.formatter as formatter
app = Flask(__name__)

@app.route('/')
def main():
   return 'Hello, World!'

@app.route('/location/<busCode>')
def location(busCode):
   '''
   Returns the location of a bus defined by a busCode
   '''
   error = False
   acceptList = request.headers.getlist('accept')
   try:
      latitude, longitude = opendata.getBusLocation(busCode)
   except ValueError:
      error = True

   if error:  
      json = {'404': 'Bus code {} not found'.format(busCode)}
      return json

   if len(acceptList) == 1:
      acceptList = acceptList[0]

   if 'application/json' in acceptList:
      json = formatter.locationJSON(busCode, longitude, latitude)
      return json
   else: # Defaults to XML response
      xml = formatter.locationXML(busCode, longitude, latitude)
      return Response(xml, mimetype='text/xml')
