from db import db
from models.lugar import Lugar

class Ruta(db.Model):
    __tablename__ = 'ruta'
    id = db.Column(db.Integer, primary_key=True)
    # relacion con la class Lugar
    id_origen = db.Column(db.Integer, db.ForeignKey('lugar.id'))
    id_destino = db.Column(db.Integer, db.ForeignKey('lugar.id'))
    # relacion con la class Combi
    id_combi = db.Column(db.Integer, db.ForeignKey('combi.id'))
    duracion_minutos = db.Column(db.Integer)
    km = db.Column(db.Integer)
    viajes = db.relationship('Viaje', backref = 'viaje')
    enabled = db.Column(db.Integer) # 1 disponible 0 no disponible

    def __init__(self, origen, destino, combi, duracion_minutos, km):
        self.id_origen = origen 
        self.id_destino = destino
        self.id_combi = combi
        self.duracion_minutos = duracion_minutos
        self.km = km
        self.enabled = 1

    def all():
        rutas = Ruta.query.all()
        return rutas

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def buscarRutaPorOrigenYDestinoYCombi(origen, destino, combi):
        ruta = Ruta.query.filter_by(id_origen=origen, id_destino=destino, id_combi=combi, enabled = 1).first()
        return ruta

    def buscarRutaPorOrigenYDestino(origen, destino):
        origen = Lugar.buscarPorLocalidad(origen)
        destino = Lugar.buscarPorLocalidad(destino)
        if (origen is not None) and (destino is not None):
            ruta = Ruta.query.filter_by(id_origen=origen.id, id_destino=destino.id, enabled=1).first()
            return ruta
        return None

    def buscarRutaPorId(id):
        ruta = Ruta.query.filter_by(id=id).first()
        return ruta

    def actualizar(self):
        db.session.commit()
        return True

    def buscarPorCombi(id_c):
        rutas = Ruta.query.filter_by(id_combi=id_c).all()
        return rutas