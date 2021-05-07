from db import db

class Combi(db.Model):
    __tablename__ = 'combi'
    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.Integer)
    anio = db.Column(db.Integer)
    modelo = db.Column(db.String(255))

    def __init__(self, patente, anio, modelo):
        self.patente = patente
        self.anio = anio
        self.modelo = modelo


    def all():
        combis = Combi.query.all()
        return combis