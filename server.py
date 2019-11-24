from flask import Flask, request, Response, jsonify, json
from flask_cors import CORS
import utils.opendata as opendata
import utils.formatter as formatter
import utils.imgur as imgur
import utils.oauth as oauth
from entities.Usuario import Usuario
from entities.Comentario import Comentario

app = Flask(__name__)
CORS(app)

@app.route('/imgurTest/upload', methods = ['POST'])
def imgurUpload():
   if request.method == 'POST': 
      image = request.form['image']
      link = imgur.uploadImage(image)
   return Response(json.dumps({'link':link}), mimetype='application/json', status=200)

@app.route('/api/v1/buses')
def allBuses():
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
def allBusesGEOJson():
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
      result = opendata.getBusLocation(busCode)
   except ValueError:
      response = {'404': 'Bus code {} not found'.format(busCode)}
      return Response(json.dumps(response), mimetype='application/json', status=404)

   if 'text/xml' in acceptList:
      response = formatter.busXML(busCode, result)
      return Response(response, mimetype='text/xml', status=200)
   else: # Defaults to JSON response
      response = formatter.busJSON(busCode, result)
      return Response(json.dumps(response), mimetype='application/json', status=200)

@app.route('/api/v1/buses/<busCode>/geojson')
def busGEOJSON(busCode):
   '''
   Returns the location of a bus defined by a busCode in GeoJSON
   '''
   try:
      result = opendata.getBusLocation(busCode)
   except ValueError:
      response = {'404': 'Bus code {} not found'.format(busCode)}
      return Response(json.dumps(response), mimetype='application/json', status=404)

   response = formatter.busGeoJSON(busCode, result)
   return Response(json.dumps(response), mimetype='application/json', status=200)

@app.route('/api/v1/stops')
def allStops():
   '''
   Returns the location of all bus stops
   '''
   result = opendata.getAllStopsLocation()
   response = formatter.stopsJSON(result)
   return Response(json.dumps(response), mimetype='application/json', status=200)

@app.route('/api/v1/stops/geojson')
def allStopsGEOJson():
   '''
   Returns the location of all bus stops
   '''
   result = opendata.getAllStopsLocation()
   response = formatter.stopsGeoJSON(result)
   return Response(json.dumps(response), mimetype='application/json', status=200)
   
@app.route('/api/v1/stops/<stopCode>')
def stop(stopCode):
   '''
   Returns the location of a bus stop define by a stopCode
   '''
   try:
      result = opendata.getOneStopLocation(stopCode)
   except ValueError:
      response = {'404': 'Stop code {} not found'.format(stopCode)}
      return Response(json.dumps(response), mimetype='application/json', status=404)

   response = formatter.stopJSON(stopCode, result)
   return Response(json.dumps(response), mimetype='application/json', status=200)

@app.route('/api/v1/stops/<stopCode>/geojson')
def stopGEOJson(stopCode):
   '''
   Returns the location of a bus stop define by a stopCode
   '''
   try:
      result = opendata.getOneStopLocation(stopCode)
   except ValueError:
      response = {'404': 'Stop code {} not found'.format(stopCode)}
      return Response(json.dumps(response), mimetype='application/json', status=404)

   response = formatter.stopGeoJSON(stopCode, result)
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
def userByEmail(email):
   '''
   User defined by email
   '''

   try:
      id, email, username = Usuario.buscarPorEmail(email)
   except ValueError:
      response = {'404': 'user {} not found'.format(email)}
      return Response(json.dumps(response), mimetype='application/json', status=404)

   user = formatter.userJSON(id, [email, username])
   return Response(json.dumps(user), mimetype='application/json', status=200)
  

@app.route('/api/v1/users')
def allUsers():
   '''
   Returns all the users
   '''
   result = Usuario.listaUsuarios()
   result = formatter.usersJSON(result)
   return Response(json.dumps(result), mimetype='application/json', status=200)

@app.route('/api/v1/comments')
def allComments():
   '''
   Returns all the commments
   '''
   result = Comentario.getComentarios()
   response = formatter.commentsJSON(result)
   return Response(json.dumps(response), mimetype='application/json', status=200)

@app.route('/api/v1/comments/<id>')
def comments(id):
   '''
   Returns the comment that has the id 
   '''
   try:
      id, usuario_id, codigoEMT, texto, imagen = Comentario.getComentarioID(id)
   except ValueError:
      response = {'404': 'Comment {} not found'.format(id)}
      return Response(json.dumps(response), mimetype='application/json', status=404)
   
   comment = formatter.commentJSON(id, [usuario_id,codigoEMT,texto,imagen])
   return Response(json.dumps(comment), mimetype='application/json', status=200)

@app.route('/api/v1/comments/userid/<userid>')
def commentByUserId(userid):
   '''
   Returns all the user's comments
   '''
   result = Comentario.getComentarioUser(userid)

   response = formatter.commentsJSON(result)
   return Response(json.dumps(response),mimetype='application/json', status=200)

@app.route('/api/v1/comments/EMTCode/<codigoEMT>')
def commentEMTEntity(codigoEMT):
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
   
@app.route('/api/v1/users', methods = ['POST'])
def user():
   if request.method == 'POST':
      try:
         user = oauth.verifyToken(request.form['idtoken'])
         Usuario.newUsuario(user['userid'], user['email'], user['name'])
         return Response(json.dumps({200:'Success'}), mimetype='application/json', status=200)
      except ValueError:
         response = {'401': 'Error validating token id'}
         return Response(json.dumps(response), mimetype='application/json', status=401)
   else:
      return Response(json.dumps({400:'Post request expected'}), mimetype='application/json', status=400)