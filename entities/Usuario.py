import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.BD import BD
from mysql.connector import Error
from flask import Flask, request, Response, jsonify, json, render_template

class Usuario:

    tabla = 'Usuario'

    def _init_(self,id: int = None, email: str = None, username: str = None):
        self.id = id
        self.email = email
        self.username = username

    def usuarioJSON(self,id, email, username):
        '''
        Converts a bus location into JSON format
        '''
        json = {
            'id': id, 
            'longitude': email,
            'latitude': username
            }
        return json

    def usersJSON(self,result):
        '''
        Converts a list of user into JSON format
        Expects a dict in the following format:
        {
            user1: (email,username),
            user2:(email,username),
            ...
        }
            '''
        json = []
        for key, value in result.items():
            json.append(usuarioJSON(key, value[0], value[1]))
        return json

    @staticmethod
    def newUsuario(id: int,email: str, username: str):
        if email == None or username == None:
            print('Error: los datos no pueden ser nulos')
            return None
        bd = BD()

        #TODO comprobar que usuario no esta en la tabla, si ya estuviera devolver error
        valores = ['null',email,username]
        bd.insert(valores,Usuario.tabla)

        lastUser = ' MAX(id) '
        user = bd.selectEscalar(lastUser,Usuario.tabla,None)
        newUser = Usuario(user[0],email,username)
        return newUser

    def listaUsuarios(self):
        bd = BD()
        condicion = None
        ap = bd.select('*',Usuario.tabla,condicion)
        #creo una lista vacia (que se usara para devolver el resultado)
        lista = []
        #cada tupla en la lista obtenida en la consulta se usa para crear una instancia de apadrinamiento y se agregan a la lista vacia
        for col in ap:
            id = col[0]
            email = col[1]
            username = col[2]
            
            user = Usuario(id, email, username)
            lista.append(user)
        return lista

    @staticmethod
    def buscarPorEmail(email: str):
        try:
            bd = BD()
            condicion = 'email = "'+email+'"'
            resultado = '*'
            myresult =  bd.select(resultado,Usuario.tabla,condicion)
            return myresult
        except Error as e:
            print(e)


if __name__ == "__main__":
    usuario = Usuario.buscarPorEmail("910tomy910@gmail.com")
    print(usuario)
   