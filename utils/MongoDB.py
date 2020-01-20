import pymongo
from bson.objectid import ObjectId
import json
'''
Usage:
No hay select con varias tablas
No hay delete o update en masa
    -Select * from users
    select({}, 'users', {})

    -Select id from users where name='pepito'
    select({'id':1}, 'users', {'name':'pepito'})

    -Insert into users values(1, 'javi@edmail', 'javi', 'http://imagen')
    insert({
        'id': 1,
        'email': 'javi@edmail',
        'username': 'javi',
        'imagen': 'http://imagen'
    }, 'users')

    -Delete from users where id = 1
    delete('users', {'id': 1})

    -Update users set id=2 where id =1
    update('users', { 'id': 2}, {'id':1})
'''

class BD:

    def __init__(self):

        credenciales, database = self.leerCredenciales()
        
        client = pymongo.MongoClient(credenciales)
        self.conn = client[database]
        print('Connected to MongoDB')


    def leerCredenciales(self):
        with open ('secrets.json') as file:
            data = json.load(file)
            credenciales = data['mongoDBConnection']
            database = data['mongoDBDatabase']

            return credenciales, database

    def select(self, resultado: str, tabla: str, condicion = {}):

        collection = self.conn[tabla]
        resultado['uselessKeySoItShowsTheRestOfThem'] = 0
        print(condicion)
        print(resultado)
        if resultado is {}:
            myresult = collection.find(condicion)
        else:
            myresult = collection.find(condicion, resultado)

        result = []
        for item in myresult:
            print(item.keys())
            tupla = ()
            for value in item:
                if isinstance(item[value], ObjectId):
                    tupla += (str(item[value]),)
                else:
                    tupla += (item[value],)
            result.append(tupla)
        return result


    def selectEscalar(self, resultado: str, tabla: str, condicion = {}):
        lista = self.select(resultado, tabla, condicion)
        if lista == None or lista == []:
            return None
        else:
            return lista[0]

    def insert(self, valores, tabla: str):
        collection = self.conn[tabla]
        collection.insert_one(valores)

    def delete(self, tabla: str, condicion = {}):
        collection = self.conn[tabla]
        collection.delete_one(condicion)

    def update(self, tabla: str, setData, condicion = {}):
        collection = self.conn[tabla]
        setData = {'$set': setData}
        collection.update_one(condicion, setData)


if __name__ == '__main__':
    bd = BD()
    print('Me he conectado')
    abc = bd.select({},'comments', {})
    print(abc)
    bd.insert({
        'id': 1,
        'email': 'javi@edmail',
        'username': 'javi',
        'imagen': 'http://imagen'
    }, 'users')

    bd.update('users', {'username': 'javipere'}, {'username': 'javi'})
    abc = bd.select({},'users', {'email': 'javi@edmail'})
    print(abc)
    bd.delete('users', {'username': 'javipere'})
    #print(abc)
