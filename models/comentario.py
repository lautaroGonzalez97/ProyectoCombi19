from db import db

class Comentario(db.Model):
    __tablename__ = 'comentario'
    id = db.Column(db.Integer, primary_key=True)
    idCliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    descripcion = db.Column(db.String(255))

    def __init__(self, idCliente, desc):
        self.idCliente = idCliente
        self.descripcion = desc


    def save(self):
        db.session.add(self)
        db.session.commit()
        return True
    
    def all():
        comentarios = Comentario.query.all()
        return comentarios