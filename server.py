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

@app.route('/api/v1/imgur/upload', methods = ['POST'])
def imgurUpload():
   if request.method == 'POST': 
      image = request.form['image']
      link = imgur.uploadImage(image)
      return Response(json.dumps({'link':link}), mimetype='application/json', status=200)
   else:
      return Response(json.dumps({400:'Post request expected'}), mimetype='application/json', status=400)

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
   acceptList = request.headers.get('accept')

   result = opendata.getAllStopsLocation()
   
   if 'text/xml' in acceptList:
      response = formatter.stopsXML(result)
      return Response(response, mimetype='text/xml', status=200)
   else: # Defaults to JSON response
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
   acceptList = request.headers.get('accept')

   try:
      result = opendata.getOneStopLocation(stopCode)
   except ValueError:
      response = {'404': 'Stop code {} not found'.format(stopCode)}
      return Response(json.dumps(response), mimetype='application/json', status=404)
   if 'text/xml' in acceptList:
      response = formatter.stopXML(stopCode, result)
      return Response(response, mimetype='text/xml', status=200)
   else: # Defaults to JSON response
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
   acceptList = request.headers.get('accept')
   try:
      result = opendata.getBusesInRoute(routeCode)
   except ValueError:
      response = {'404': 'Route code {} not found'.format(routeCode)}
      return Response(json.dumps(response), mimetype='application/json', status=404)

   if 'text/xml' in acceptList:
      response = formatter.busesXML(result)
      return Response(response, mimetype='text/xml', status=200)
   else: # Defaults to JSON response
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
   acceptList = request.headers.get('accept')

   try:
      id, email, username, image = Usuario.buscarPorEmail(email)
   except ValueError:
      response = {'404': 'user {} not found'.format(email)}
      return Response(json.dumps(response), mimetype='application/json', status=404)

   if 'text/xml' in acceptList:
      response = formatter.userXML(id, [email, username, image])
      return Response(response, mimetype='text/xml', status=200)
   else: # Defaults to JSON response
      user = formatter.userJSON(id, [email, username, image])
      return Response(json.dumps(user), mimetype='application/json', status=200)
  

@app.route('/api/v1/users')
def allUsers():
   '''
   Returns all the users
   '''
   acceptList = request.headers.get('accept')

   result = Usuario.listaUsuarios()

   if 'text/xml' in acceptList:
      response = formatter.usersXML(result)
      return Response(response, mimetype='text/xml', status=200)
   else: # Defaults to JSON response
      result = formatter.usersJSON(result)
      return Response(json.dumps(result), mimetype='application/json', status=200)

@app.route('/api/v1/comments', methods = ['POST', 'GET'])
def allComments():
   '''
   Returns all the commments
   '''
   if request.method == 'GET':
      acceptList = request.headers.get('accept')

      result = Comentario.getComentarios()
      
      if 'text/xml' in acceptList:
         response = formatter.commentsXML(result)
         return Response(response, mimetype='text/xml', status=200)
      else: # Defaults to JSON response
         response = formatter.commentsJSON(result)
         return Response(json.dumps(response), mimetype='application/json', status=200)
   elif request.method == 'POST':
      try:
         userId = request.form['userToken']
         userId = oauth.verifyToken(userId)['userid']
         body = request.form['body']
         image = request.form['image']
         link = imgur.uploadImage(image)
         emtCode = request.form['emtCode']

         Comentario.newComentario(userId, emtCode, body, link)
         return Response(json.dumps({200:'Success'}), mimetype='application/json', status=200)
      except ValueError:
         response = {'401': 'Error adding new comment'}
         return Response(json.dumps(response), mimetype='application/json', status=401)

@app.route('/api/v1/comments/<id>')
def comments(id):
   '''
   Returns the comment that has the id 
   '''
   acceptList = request.headers.get('accept')

   try:
      id, usuario_id, codigoEMT, texto, imagen = Comentario.getComentarioID(id)
   except ValueError:
      response = {'404': 'Comment {} not found'.format(id)}
      return Response(json.dumps(response), mimetype='application/json', status=404)

   if 'text/xml' in acceptList:
      response = formatter.commentXML(id, [usuario_id,codigoEMT,texto,imagen])
      return Response(response, mimetype='text/xml', status=200)
   else: # Defaults to JSON response
      comment = formatter.commentJSON(id, [usuario_id,codigoEMT,texto,imagen])
      return Response(json.dumps(comment), mimetype='application/json', status=200)

@app.route('/api/v1/comments/userid/<userid>')
def commentByUserId(userid):
   '''
   Returns all the user's comments
   '''
   acceptList = request.headers.get('accept')

   result = Comentario.getComentarioUser(userid)

   if 'text/xml' in acceptList:
      response = formatter.commentsXML(result)
      return Response(response, mimetype='text/xml', status=200)
   else: # Defaults to JSON response
      response = formatter.commentsJSON(result)
      return Response(json.dumps(response),mimetype='application/json', status=200)

@app.route('/api/v1/comments/EMTCode/<codigoEMT>')
def commentEMTEntity(codigoEMT):
   '''
   Returns all the stop or bus' comments
   '''
   acceptList = request.headers.get('accept')

   result = Comentario.getComentarioEMT(codigoEMT)

   if 'text/xml' in acceptList:
      response = formatter.commentsXML(result)
      return Response(response, mimetype='text/xml', status=200)
   else: # Defaults to JSON response
      response = formatter.commentsJSON(result)
      return Response(json.dumps(response),mimetype='application/json', status=200)

@app.route('/api/v1/comments/user/<username>')
def commentStopUsernameJSON(username):
   '''
   Returns all the stop or bus' comments of a user
   '''
   acceptList = request.headers.get('accept')

   result = Comentario.getComentarioByUsername(username)

   if 'text/xml' in acceptList:
      response = formatter.commentsXML(result)
      return Response(response, mimetype='text/xml', status=200)
   else: # Defaults to JSON response
      response = formatter.commentsJSON(result)
      return Response(json.dumps(response),mimetype='application/json', status=200)
   
@app.route('/api/v1/users', methods = ['POST'])
def user():
   if request.method == 'POST':
      try:
         user = oauth.verifyToken(request.form['idtoken'])
         Usuario.newUsuario(user['userid'], user['email'], user['name'], user['image'])
         return Response(json.dumps({200:'Success'}), mimetype='application/json', status=200)
      except ValueError:
         response = {'401': 'Error validating token id'}
         return Response(json.dumps(response), mimetype='application/json', status=401)
   else:
      return Response(json.dumps({400:'Post request expected'}), mimetype='application/json', status=400)
