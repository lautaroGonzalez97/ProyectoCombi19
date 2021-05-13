from sqlalchemy.orm import backref
from db import db

class Lugar(db.Model):
    __tablename__ = 'lugar'
    id = db.Column(db.Integer, primary_key=True)
    localidad = db.Column(db.String(255))
    provincia = db.Column(db.String(255))
    origen = db.relationship('Ruta', backref='origen', foreign_keys="Ruta.id_origen")
    destino = db.relationship('Ruta', backref='destino', foreign_keys="Ruta.id_destino")

    def __init__(self, localidad, provincia):
        self.localidad = localidad
        self.provincia = provincia

    def all():
        lugares = Lugar.query.all()
        return lugares

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def actualizar(self):
        db.session.commit()
        return True

    def buscarPorLocalidadYProvincia(loc, prov):
        lugar = Lugar.query.filter_by(localidad=loc, provincia=prov).first()
        return lugar

    def buscarLugarPorId(id):
        lugar = Lugar.query.filter_by(id=id).first()
        return lugar

    def eliminar_lugar(lugar):
        db.session.delete(lugar)
        db.session.commit()
        return True
