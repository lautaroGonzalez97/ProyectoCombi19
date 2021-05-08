from db import db

class Lugar(db.Model):
    __tablename__ = 'lugar'
    id = db.Column(db.Integer, primary_key=True)
    localidad = db.Column(db.String(255))
    provincia = db.Column(db.String(255))

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

    def actualizar(id):
        db.session.commit()
        return True

    def buscarPorLocalidadYProvincia(loc, prov):
        lugar = Lugar.query.filter_by(localidad=loc, provincia=prov).first()
        return lugar

    def buscarLugarPorId(id):
        lugar = Lugar.query.filter_by(id=id).first()
        return lugar