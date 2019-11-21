from flask import Flask, request, Response, jsonify, json, render_template
import utils.opendata as opendata
import utils.formatter as formatter
import utils.darksky as darksky
from entities.Usuario import Usuario
from entities.Comentario import Comentario
app = Flask(__name__)

@app.route('/')
def main():
   '''
   Adds forecast data and renders the main page
   '''
   tempMax, tempMin, summary, icon = darksky.todayForecast(darksky.malaga_lat, darksky.malaga_lon)
   temps = str(tempMax) + '~' + str(tempMin)
   icon = darksky.iconMapping[icon]
   return render_template('index.html',
      temperature=temps, summary=summary, weatherIcon=icon)

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

@app.route('/api/v1/stops/geojson')
def locationAllStopsGeoJSON():
   '''
   Returns the location of all bus stops
   '''
   result = opendata.getAllStopsLocation()
   response = formatter.stopsGeoJSON(result)
   return Response(json.dumps(response), mimetype='application/json', status=200)
   
@app.route('/api/v1/stops/<stopCode>')
def locationOneStop(stopCode):
   '''
   Returns the location of a bus stop define by a stopCode
   '''
   try:
      name, lat, lon = opendata.getOneStopLocation(stopCode)
   except ValueError:
      response = {'404': 'Stop code {} not found'.format(stopCode)}
      return Response(json.dumps(response), mimetype='application/json', status=404)

   response = formatter.stopJSON(stopCode, name, lat, lon)
   return Response(json.dumps(response), mimetype='application/json', status=200)

@app.route('/api/v1/stops/<stopCode>/geojson')
def locationOneStopGeoJSON(stopCode):
   '''
   Returns the location of a bus stop define by a stopCode
   '''
   try:
      name, lat, lon = opendata.getOneStopLocation(stopCode)
   except ValueError:
      response = {'404': 'Stop code {} not found'.format(stopCode)}
      return Response(json.dumps(response), mimetype='application/json', status=404)

   response = formatter.stopGeoJSON(stopCode, name, lat, lon)
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
	response = formatter.busesJSON(result)
	return Response(json.dumps(response), mimetype='application/json', status=200)

@app.route('/api/v1/routes/<routeCode>/geojson')
def busesInRouteGeoJson(routeCode):
	'''
	Returns the location of all buses in a route
	'''	
	try:
		result = opendata.getBusesInRoute(routeCode)
	except ValueError:
		response = {'404': 'Route code {} not found'.format(routeCode)}
		return Response(json.dumps(response), mimetype='application/json', status=404)
	response = formatter.busesGeoJSON(result)
	return Response(json.dumps(response), mimetype='application/json', status=200)

@app.route('/api/v1/users/<email>')
def userByEmailJSON(email):
   '''
   Usuario con email concreto
   '''

   try:
      id, email, username = Usuario.buscarPorEmail(email)
   except ValueError:
      response = {'404': 'user {} not found'.format(email)}
      return Response(json.dumps(response), mimetype='application/json', status=404)

   user = Usuario.usuarioJSON(id, email, username)
   return Response(json.dumps(user), mimetype='application/json', status=200)
  

@app.route('/api/v1/users')
def allUsersJSON():
   '''
   Returns all the users
   '''
   result = Usuario.listaUsuarios()
   return Response(json.dumps(result), mimetype='application/json', status=200)

@app.route('/api/v1/comments')
def allCommentsJSON():
   '''
   Returns all the commments
   '''
   result = Comentario.getComentarios()
   response = formatter.commentsJSON(result)
   return Response(json.dumps(response), mimetype='application/json', status=200)

@app.route('/api/v1/comment/<id>')
def commentJSON(id):
   '''
   Returns the comment that has the id 
   '''
   try:
      id, usuario_id, codigoEMT, texto, imagen = Comentario.getComentarioID(id)
   except ValueError:
      response = {'404': 'Comment {} not found'.format(id)}
      return Response(json.dumps(response), mimetype='application/json', status=200)
   
   comment = formatter.commentJSON(id,usuario_id,codigoEMT,texto,imagen)
   return Response(json.dumps(comment), mimetype='application/json', status=200)

@app.route('/api/v1/comments/userid/<userid>')
def commentUserJSON(userid):
   '''
   Returns all the user's comments
   '''
   result = Comentario.getComentarioUser(userid)

   response = formatter.commentsJSON(result)
   return Response(json.dumps(response),mimetype='application/json', status=200)

@app.route('/api/v1/comments/codigoEMT/<codigoEMT>')
def commentStopJSON(codigoEMT):
   '''
   Returns all the stop or bus' comments
   '''
   result = Comentario.getComentarioEMT(codigoEMT)

   response = formatter.commentsJSON(result)
   return Response(json.dumps(response),mimetype='application/json', status=200)

@app.route('/api/v1/comments/user/<username>')
def commentStopUsernameJSON(username):
   '''
   Returns all the stop or bus' comments of a user
   '''
   result = Comentario.getComentarioByUsername(username)

   response = formatter.commentsJSON(result)
   return Response(json.dumps(response),mimetype='application/json', status=200)
   

def error(code, message):
   response = {
      code : message
   }
   return Response(json.dumps(response), mimetype='application/json', status=404)