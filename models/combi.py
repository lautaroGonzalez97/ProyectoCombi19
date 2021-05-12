from db import db

class Combi(db.Model):
    __tablename__ = 'combi'
    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(255))
    modelo = db.Column(db.String(255))
    asientos = db.Column(db.Integer)
    tipo = db.Column(db.String(255))
    # relacion con la class Personal
    id_chofer = db.Column(db.Integer, db.ForeignKey('personal.id'))
    # relacion con la class Ruta
    rutas = db.relationship('Ruta', backref='ruta')

    def __init__(self, patente, modelo, asientos, tipo, id_chofer):
        self.patente = patente
        self.modelo = modelo
        self.asientos = asientos
        self.tipo = tipo
        self.id_chofer = id_chofer

    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def all():
        combis = Combi.query.all()
        return combis

    def buscarCombiPorId(id):
        combi = Combi.query.filter_by(id=id).first()
        return combi

    def actualizar(id):
        db.session.commit()
        return True

    def eliminar_combi(combi):
        db.session.delete(combi)
        db.session.commit()
        return True