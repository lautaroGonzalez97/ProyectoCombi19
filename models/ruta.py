from db import db

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

    def __init__(self, origen, destino, combi, duracion_minutos, km):
        self.id_origen = origen 
        self.id_destino = destino
        self.id_combi = combi
        self.duracion_minutos = duracion_minutos
        self.km = km

    def all():
        rutas = Ruta.query.all()
        return rutas

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def buscarRutaPorOrigenYDestino(origen, destino):
        ruta = Ruta.query.filter_by(id_origen=origen, id_destino=destino).first()
        return ruta

    def buscarRutaPorId(id):
        ruta = Ruta.query.filter_by(id=id).first()
        return ruta

    def actualizar(self):
        db.session.commit()
        return True