from db import db
from models.viaje import Viaje
metadata = db.MetaData()

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    apellido = db.Column(db.String(255))
    email = db.Column(db.String(255))
    fechaNacimiento = db.Column(db.Date())
    password = db.Column(db.String(255))
    tarjetas = db.relationship('Tarjeta', backref='tarjeta')
    comentarios = db.relationship('Comentario', backref='comentario')

    '''association_table = db.Table('cliente_compra_viaje', metadata, 
                                db.Column('cliente_id',  db.Integer, db.ForeignKey(id)), 
                                db.Column('viaje_id', db.Integer, db.ForeignKey(Viaje.id)),
                                db.Column('estado', db.Integer))

    viajes = db.relationship("Viaje", secondary=association_table,)'''

    def __init__(self, nombre, apellido, email, fechaNacimiento, password):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.fechaNacimiento = fechaNacimiento
        self.password = password

    def idUsuario(self):
        client = self.query.filter_by(email=self.email)
        idClient = client.first().id
        return idClient

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def buscarEmailPassword(unEmail, unaPass):
        client = Cliente.query.filter_by(email=unEmail, password=unaPass)
        if (client.count() == 1):
            return client.first().idUsuario()
        else:
            return None
            
    def buscarPorEmail(email):
        client = Cliente.query.filter_by(email=email).first()
        return client

    def buscarPorId(id):
        client = Cliente.query.filter_by(id=id).first()
        return client

    def actualizar (self):
        db.session.commit()
        return True
