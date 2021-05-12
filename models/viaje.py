from db import db

class Viaje(db.Model):
    __tablename__ = 'viaje'
    id = db.Column(db.Integer, primary_key = True)
    id_ruta = db.Column(db.Integer, db.ForeignKey('ruta.id'))
    asientos_disponibles = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    precio = db.Column(db.Float)

    def __init__(self, id_ruta, asientos_disponibles, fecha, precio):
        self.id_ruta = id_ruta
        self.asientos_disponibles=asientos_disponibles
        self.fecha=fecha
        self.precio=precio

    def all():
        viajes = Viaje.query.all()
        return viajes

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def buscarViajePorId(id):
        viaje = Viaje.query.filter_by(id=id).first()
        return viaje

    def eliminar_viaje(viaje):
        db.session.delete(viaje)
        db.session.commit()
        return True

        