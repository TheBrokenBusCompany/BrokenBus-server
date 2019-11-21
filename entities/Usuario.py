import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.BD import BD
from mysql.connector import Error
from flask import Flask, request, Response, jsonify, json, render_template

class Usuario:

    tabla = 'Usuario'

    def __init__(self,id: int = None, email: str = None, username: str = None):
        self.id = id
        self.email = email
        self.username = username


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

    @staticmethod
    def getUsuario(id: int, email: str,username: str):
        bd = BD()
        condicion = 'id = ' + str(id) + ' and email = "' + email + '" and username = "' + username + '"'
        resultado = '*'

        consulta = bd.selectEscalar(resultado ,Usuario.tabla, condicion)
        if consulta != None:
            newUser = Usuario(consulta[0], consulta[1], consulta[2])
            return newUser
        else:
            print('Usuario erróneo')
            return None

    
    def deleteUser(self):
        bd = BD()
        condicion = 'id = ' + str(self.id) + ' and email = "' + self.email + '" and username = "' + self.username + '"'
        bd.delete(Usuario.tabla, condicion)
        self.id = None
        self.email = None
        self.username = None

    @staticmethod  
    def listaUsuarios():
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
            
            user = Usuario.usuarioJSON(id, email, username)
            lista.append(user)
        return lista

    @staticmethod
    def buscarPorEmail(email):
        try:
            bd = BD()
            condicion = 'email = "'+email+'"'
            resultado = '*'
            [(id, email, username)] =  bd.select(resultado,Usuario.tabla,condicion)
            return id, email, username
        except Error:
            raise ValueError('User not found')

if __name__ == "__main__":
    print(Usuario.buscarPorEmail('910tomy910@gmail.com'))
   