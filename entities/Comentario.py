import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.BD import BD
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
    def newComentario (id: int, usuario_id: int, codigoEMT: str, texto: str = None, imagen: str = None):
        bd = BD()
        condicion = 'id = ' + str(usuario_id)
        resultado = '*'
        consulta = bd.selectEscalar(resultado, Comentario.tablaUsuarios, condicion)
        if consulta != None:
            #Usuario existente

            valores = [id,usuario_id, codigoEMT, texto, imagen]
            bd.insert(valores, Comentario.tabla)

            newComment = Comentario(id,usuario_id, codigoEMT, texto, imagen)
            print(newComment)
            return newComment
            
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
    comentario = Comentario.getComentario(1,1,'P1')
    print(comentario)
    comentario.deleteComentario()
    
