from sqlalchemy.orm import query
from db import db

class Viaje(db.Model):
    __tablename__ = 'viaje'
    id = db.Column(db.Integer, primary_key = True)
    id_ruta = db.Column(db.Integer, db.ForeignKey('ruta.id'))
    asientos_disponibles = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    horaSalida = db.Column (db.Time())
    horaLlegada = db.Column (db.Time())
    precio = db.Column(db.Float)
    estado = db.Column(db.Integer)
    asientos = db.Column(db.Integer)
    enabled = db.Column(db.Integer)

    def __init__(self, id_ruta, asientos_disponibles, fecha, horaSalida, horaLlegada, precio, estado):
        self.id_ruta = id_ruta
        self.asientos_disponibles=asientos_disponibles
        self.fecha=fecha
        self.horaSalida= horaSalida
        self.horaLlegada= horaLlegada
        self.precio=precio
        self.estado=estado    # 1 = pendiente     2= en curso     3= finalizado
        self.asientos = self.asientos_disponibles
        self.enabled = 1 

    def all():
        viajes = Viaje.query.all()
        return viajes

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def actualizar(self):
        db.session.commit()
        return True

    def buscarViajePorId(id):
        viaje = Viaje.query.filter_by(id=id).first()
        return viaje