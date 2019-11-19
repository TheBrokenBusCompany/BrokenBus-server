from utils.BD import BD
import sys

class Comentario:
    tabla = 'Comentario'

    def __init__ (self, usuario_id: int = None, entidadEMT_id: int = None, texto: str = None, imagen: str = None):
        self.usuario_id = usuario_id
        self.entidadEMT_id = entidadEMT_id
        self.texto = texto
        self.imagen = imagen

    @staticmethod
    def newComentario (usuario_id: int, entidadEMT_id: int, texto: str = None, imagen: str = None):
        bd = BD()
        condicion = 'usuario_id = ' + str(usuario_id)
        resultado = '*'
        consulta = bd.selectEscalar(resultado, Comentario.tabla, condicion)
        if consulta != None:
            #Usuario existente
            condicion = 'entidadEMT_id = ' + entidadEMT_id
            consulta = bd.selectEscalar(resultado, Comentario.tabla, condicion)
            if consulta:
                valores = [usuario_id, entidadEMT_id, texto, imagen]
                bd.insert(valores, Comentario.tabla)

                newComment = Comentario(usuario_id, entidadEMT_id, texto, imagen)
                print(newComment)
                return newComment
            else:
                print('Bus o Parada Inexistente')
                return None
        else:
            print('Usuario inexistente')
            return None

    @staticmethod
    def getComentario (usuario_id: int, entidadEMT_id: int):
        bd = BD()
        condicion = 'usuario_id = ' + usuario_id + ' and entidadEMT_id = ' + entidadEMT_id
        resultado = '*'

        consulta = bd.select(resultado ,Comentario.tabla, condicion)
        if consulta != None:
            return consulta
        else:
            print('Usuario o Comentario erróneos')
            return None

    @staticmethod
    def deleteComentario(self)
        
        

