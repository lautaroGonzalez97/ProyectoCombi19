from db import db

class Combi(db.Model):
    __tablename__ = 'combi'
    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(255))
    modelo = db.Column(db.String(255))
    asientos = db.Column(db.Integer)
    tipo = db.Column(db.String(255))
    id_chofer = db.Column(db.Integer, db.ForeignKey('personal.id'))

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