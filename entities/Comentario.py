import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.MongoDB import BD

class Comentario:
    tabla = 'comments'
    tablaUsuarios = 'users'

    def __init__ (self, id: int, usuario_id: int = None, codeEMT: str = None, texto: str = None, imagen: str = None):
        self.id = id
        self.usuario_id = usuario_id
        self.codeEMT = codeEMT
        self.texto = texto
        self.imagen = imagen

    @staticmethod
    def newComentario (usuario_id: int, codeEMT: str, text: str = None, imagen: str = None):
        bd = BD()
        condicion = {'_id': usuario_id}
        resultado = {}
        consulta = bd.selectEscalar(resultado, Comentario.tablaUsuarios, condicion)
        if consulta != None:
            #Usuario existente

            valores = {
                'user_id': usuario_id,
                'codeEMT': codeEMT,
                'text': text,
                'image': imagen
            }
            bd.insert(valores, Comentario.tabla)


        else:
            print('Usuario inexistente')
            return None

    @staticmethod
    def getComentario (id: int, usuario_id: int, codeEMT: str):
        bd = BD()
        condicion = {'_id': id,
        'user_id':usuario_id,
        'codeEMT': codeEMT}
        resultado = {}

        consulta = bd.selectEscalar(resultado ,Comentario.tabla, condicion)
        if consulta != None:
            newComment = Comentario(consulta[0], consulta[1], consulta[2],consulta[3],consulta[4])
            return newComment
        else:
            print('Usuario o Comentario erróneos')
            return None

    @staticmethod
    def getComentarios():
        bd = BD()
        condicion = {}
        resultado = {}

        consulta = bd.select(resultado,Comentario.tabla, condicion)
        
        return consulta

    @staticmethod
    def getComentarioID(id):
        bd = BD()
        condicion = {'_id':id}
        resultado = {}
        try:
            [(id,usuario_id,codeEMT,texto,imagen)] = bd.select(resultado,Comentario.tabla, condicion)
            return id,usuario_id,codeEMT,texto,imagen
        except Error:
            raise ValueError('ID inexistente')

    @staticmethod
    def getComentarioUser(userid):
        bd = BD()
        condicion = {'user_id': userid}
        resultado = {}

        consulta = bd.select(resultado,Comentario.tabla,condicion)
        return consulta
    
    @staticmethod
    def getComentarioEMT(codeEMT):
        bd = BD()
        condicion = {'codeEMT': codeEMT}
        resultado = {}

        consulta = bd.select(resultado,Comentario.tabla,condicion)
        return consulta

    @staticmethod
    def getComentarioByUsername(username):
        #a primera tabla y b segunda
        bd = BD()
        ID = bd.selectEscalar({'id': 1}, Comentario.tablaUsuarios, {'username': username})
        consulta = bd.select({}, Comentario.tabla, {'user_id': ID})
        return consulta 

    def deleteComentario(self):
        bd = BD()
        condicion = {'_id': self.id}
        bd.delete(Comentario.tabla, condicion)
        self.id = None
        self.usuario_id = None
        self.codeEMT = None
        self.texto = None
        self.imagen = None
        

if __name__ == "__main__":
    #Comentario.newComentario(1,1,'P1','No funciona boton')
    Comentario.getComentarios()
    
