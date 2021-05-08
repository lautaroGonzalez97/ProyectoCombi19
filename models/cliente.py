from db import db
from models.tarjeta import Tarjeta
metadata = db.MetaData()

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    apellido = db.Column(db.String(255))
    email = db.Column(db.String(255))
    fechaNacimiento = db.Column(db.DateTime())
    password = db.Column(db.String(255))
    #disponible = db.Column(db.Integer)
    tarjetas = db.relationship('Tarjeta', backref='tarjeta')

    def __init__(self, nombre, apellido, email, fechaNacimiento, password):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.fechaNacimiento = fechaNacimiento
        self.password = password
        #disponible = 1

    #aca van las asociaciones entre las tablas, averiguar


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