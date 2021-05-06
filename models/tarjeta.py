from db import db

class  Tarjeta (db.Model):
    __tablename__ = "terjeta_credito"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    numero = db.Column(db.Integer)
    codigo = db.Column(db.Integer)
    fechaVencimiento = db.Column(db.DateTime())

    def __init__(self, nombre, numero, codigoSeguridad, fechaVencimiento):
        self.nombre = nombre
        self.numero = numero
        self.codigo = codigoSeguridad
        self.fechaVencimiento = fechaVencimiento
        
    
