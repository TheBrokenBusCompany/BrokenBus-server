import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.MongoDB import BD
from flask import Flask, request, Response, jsonify, json, render_template
import utils.formatter as formatter

class Usuario:

    tabla = 'users'

    def __init__(self,id: int = None, email: str = None, username: str = None, image: str = None):
        self.id = id
        self.email = email
        self.username = username
        self.image = image


    @staticmethod
    def newUsuario(id: str,email: str, username: str, image: str):
        if email == None or username == None:
            print('Error: los datos no pueden ser nulos')
            return None
        bd = BD()

        existe = bd.select({},Usuario.tabla,{"email": email})

        if not existe:
            valores = [id,email,username, image]
            bd.insert({"_id":id,
            "email":email,
            "username": username,
            "image": image},Usuario.tabla)
            
            newUser = Usuario(id,email,username, image)
            return newUser
        else:
            print('Usuario con email  ', email, ' ya registrado')
            return None

    #metodo que comprueba si la condicion pasada como parametro devuelve tuplas en la query o si esta devuele un nulo 
    #el resultado es verdadero si se devuelve una tupla (o una lista de tuplas) y falso si no se encuentran tuplas
    #@staticmethod
    #def estaEnLaTabla(tabla: str, condicion: str):
    #    bd = BD()
    #    resultado = '*'
    #    ap = bd.selectEscalar(resultado,tabla,condicion)
    #    return ap != None

    @staticmethod
    def getUsuario(id: str, email: str,username: str):
        bd = BD()
        condicion = {"_id":id,
            "email":email,
            "username": username}
        resultado = {}

        consulta = bd.selectEscalar(resultado ,Usuario.tabla, condicion)
        if consulta != None:
            newUser = Usuario(consulta[0], consulta[1], consulta[2], consulta[3])
            return newUser
        else:
            print('Usuario erróneo')
            return None

    
    def deleteUser(self):
        bd = BD()
        condicion = {"_id":self.id,
            "email":self.email,
            "username": self.username}
        bd.delete(Usuario.tabla, condicion)
        self.id = None
        self.email = None
        self.username = None

    @staticmethod  
    def listaUsuarios():
        bd = BD()
        ap = bd.select({},Usuario.tabla,{})
        #creo una lista vacia (que se usara para devolver el resultado)
        lista = []
        #cada tupla en la lista obtenida en la consulta se usa para crear una instancia de apadrinamiento y se agregan a la lista vacia
        for user in ap:
            lista.append(user)
        return lista

    @staticmethod
    def buscarPorEmail(email):
        try:
            bd = BD()
            condicion = {'email': email}
            resultado = {}
            [(id, email, username, image)] =  bd.select(resultado,Usuario.tabla,condicion)
            return id, email, username, image
        except ValueError:
            raise ValueError('User not found')

    @staticmethod
    def buscarPorID(id):
        try:
            bd = BD()
            condicion = {'_id': id}
            resultado = {}
            [(id, email, username, image)] =  bd.select(resultado,Usuario.tabla,condicion)
            return id, email, username, image
        except ValueError:
            raise ValueError('User not found')

if __name__ == "__main__":
    print(Usuario.buscarPorEmail('910tomy910@gmail.com'))
   