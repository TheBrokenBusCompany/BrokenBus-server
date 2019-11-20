from flask import Flask, request, Response, jsonify, json, render_template
import utils.opendata as opendata
import utils.formatter as formatter
import entities.Usuario as Usuario
app = Flask(__name__)

@app.route('/')
def main():
   return render_template('index.html')

@app.route('/api/v1/buses')
def busesAll():
   '''
   Returns the location of all buses
   '''
   acceptList = request.headers.get('accept')

   result = opendata.getBusLocations()

   if 'text/xml' in acceptList:
      response = formatter.busesXML(result)
      return Response(response, mimetype='text/xml', status=200)
   else: # Defaults to JSON response
      response = formatter.busesJSON(result)
      return Response(json.dumps(response), mimetype='application/json', status=200)

@app.route('/api/v1/buses/geojson')
def geoJsonAllBuses():
   '''
   Returns the location of all buses in GeoJSON
   '''
   result = opendata.getBusLocations()

   response = formatter.busesGeoJSON(result)

   return Response(json.dumps(response), mimetype='application/json', status=200)

@app.route('/api/v1/buses/<busCode>')
def bus(busCode):
   '''
   Returns the location of a bus defined by a busCode
   '''
   acceptList = request.headers.get('accept')
   
   try:
      latitude, longitude = opendata.getBusLocation(busCode)
   except ValueError:
      response = {'404': 'Bus code {} not found'.format(busCode)}
      return Response(json.dumps(response), mimetype='application/json', status=404)

   if 'text/xml' in acceptList:
      response = formatter.busXML(busCode, latitude, longitude)
      return Response(response, mimetype='text/xml', status=200)
   else: # Defaults to JSON response
      response = formatter.busJSON(busCode, latitude, longitude)
      return Response(json.dumps(response), mimetype='application/json', status=200)

@app.route('/api/v1/buses/<busCode>/geojson')
def geoJsonOneBus(busCode):
   '''
   Returns the location of a bus defined by a busCode in GeoJSON
   '''
   try:
      latitude, longitude = opendata.getBusLocation(busCode)
   except ValueError:
      return error(404, 'Bus code {} not found'.format(busCode))

   response = formatter.busGeoJSON(busCode, latitude, longitude)
   return Response(json.dumps(response), mimetype='application/json', status=200)

@app.route('/api/v1/stops')
def locationAllStops():
   '''
   Returns the location of all bus stops
   '''
   result = opendata.getAllStopsLocation()
   response = formatter.stopsJSON(result)
   return Response(json.dumps(response), mimetype='application/json', status=200)
   
   
@app.route('/api/v1/stops/<stopCode>')
def locationOneStop(stopCode):
	'''
	Returns the location of a bus stop define by a stopCode
	'''
	try:
		name, lon, lat = opendata.getOneStopLocation(stopCode)
	except ValueError:
		response = {'404': 'Stop code {} not found'.format(stopCode)}
		return Response(json.dumps(response), mimetype='application/json', status=404)
	response = formatter.stopJSON(stopCode, name, lon, lat)
	return Response(json.dumps(response), mimetype='application/json', status=200)
	
@app.route('/api/v1/routes/<routeCode>')
def busesInRoute(routeCode):
	'''
	Returns the location of all buses in a route
	'''	
	try:
		result = opendata.getBusesInRoute(routeCode)
	except ValueError:
		response = {'404': 'Route code {} not found'.format(routeCode)}
		return Response(json.dumps(response), mimetype='application/json', status=404)
	response = formatter.locationsJSON(result)
	return Response(json.dumps(response), mimetype='application/json', status=200)


@app.route('/api/v1/users/<email>')
def userByEmailJSON(email):
   '''
   Usuario con email concreto
   '''

   try:
      id, email, username = Usuario.buscarPorEmail(email)
   except ValueError:
      response = {'404': 'Bus code {} not found'.format(email)}
   return Response(json.dumps(response), mimetype='application/json', status=404)

@app.route('/api/v1/users')
def allUsersJSON():
   '''
   Returns all the users
   '''
   result = Usuario.getAllUsers()
   response = Usuario.usersJSON(result)
   return Response(json.dumps(response), mimetype='application/json', status=200)

def error(code, message):
   response = {
      code : message
   }
   return Response(json.dumps(response), mimetype='application/json', status=404)