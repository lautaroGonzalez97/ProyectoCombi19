from db import db

class Comentario(db.Model):
    __tablename__ = 'comentario'
    id = db.Column(db.Integer, primary_key=True)
    idCliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    fecha = db.Column(db.Date())
    descripcion = db.Column(db.String(255))

    def __init__(self, idCliente, desc, fecha):
        self.idCliente = idCliente
        self.descripcion = desc
        self.fecha = fecha


    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def actualizar(self):
        db.session.commit()
        return True
    
    def all():
        comentarios = Comentario.query.all()
        return comentarios
    
    def devolverpaginado(page):
        return Comentario.query.paginate(page, 5, False)

    def buscarComentarioPorId(id):
        comentario = Comentario.query.filter_by(id=id).first()
        return comentario

    def eliminar_comentario(comentario):
        db.session.delete(comentario)
        db.session.commit()
        return True