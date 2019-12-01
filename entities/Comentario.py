import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.BD import BD
from mysql.connector import Error

class Comentario:
    tabla = 'Comentario'
    tablaUsuarios = 'Usuario'

    def __init__ (self, id: int, usuario_id: int = None, codigoEMT: str = None, texto: str = None, imagen: str = None):
        self.id = id
        self.usuario_id = usuario_id
        self.codigoEMT = codigoEMT
        self.texto = texto
        self.imagen = imagen

    @staticmethod
    def newComentario (usuario_id: int, codigoEMT: str, texto: str = None, imagen: str = None):
        bd = BD()
        condicion = 'id = ' + str(usuario_id)
        resultado = '*'
        consulta = bd.selectEscalar(resultado, Comentario.tablaUsuarios, condicion)
        if consulta != None:
            #Usuario existente

            valores = [0, usuario_id, codigoEMT, texto, imagen]
            bd.insert(valores, Comentario.tabla)


        else:
            print('Usuario inexistente')
            return None

    @staticmethod
    def getComentario (id: int, usuario_id: int, codigoEMT: str):
        bd = BD()
        condicion = 'id = ' + str(id) + ' and usuario_id = ' + str(usuario_id) + ' and codigoEMT = "' + codigoEMT + '"'
        resultado = '*'

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
        condicion = None
        resultado = '*'

        consulta = bd.select(resultado,Comentario.tabla, condicion)
        
        return consulta

    @staticmethod
    def getComentarioID(id):
        bd = BD()
        condicion = 'id = ' + str(id)
        resultado = '*'
        try:
            [(id,usuario_id,codigoEMT,texto,imagen)] = bd.select(resultado,Comentario.tabla, condicion)
            return id,usuario_id,codigoEMT,texto,imagen
        except Error:
            raise ValueError('ID inexistente')

    @staticmethod
    def getComentarioUser(userid):
        bd = BD()
        condicion = 'usuario_id = ' + str(userid)
        resultado = '*'

        consulta = bd.select(resultado,Comentario.tabla,condicion)
        return consulta
    
    @staticmethod
    def getComentarioEMT(codigoEMT):
        bd = BD()
        condicion = 'codigoEMT = "' + codigoEMT + '"'
        resultado = '*'

        consulta = bd.select(resultado,Comentario.tabla,condicion)
        return consulta

    @staticmethod
    def getComentarioByUsername(username):
        #a primera tabla y b segunda
        bd = BD()
        condicion = 'b.id=a.usuario_id and b.username ="' + username + '"'
        resultado = 'a.id,a.usuario_id,a.codigoEMT,a.texto,a.imagen'
        consulta = bd.superSelect(resultado,Comentario.tabla,Comentario.tablaUsuarios,condicion)
        return consulta 

    def deleteComentario(self):
        bd = BD()
        condicion = 'id = ' + str(self.id) + ' and usuario_id = ' + str(self.usuario_id) + ' and codigoEMT = "' + self.codigoEMT + '"'
        bd.delete(Comentario.tabla, condicion)
        self.id = None
        self.usuario_id = None
        self.codigoEMT = None
        self.texto = None
        self.imagen = None
        

if __name__ == "__main__":
    #Comentario.newComentario(1,1,'P1','No funciona boton')
    Comentario.getComentarios()
    
