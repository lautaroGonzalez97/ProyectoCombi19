from db import db

class Insumo(db.Model):
    __tablename__ = "insumo"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    tipo = db.Column(db.String(255))
    precio = db.Column(db.Integer)

    def __init__(self, nombre, tipo, precio):
        self.nombre = nombre
        self.tipo = tipo
        self.precio = precio

    def all():
        insumos = Insumo.query.all()
        return insumos

    
    def buscarInsumoPorId(id):
        insumo = Insumo.query.filter_by(id=id).first()
        return insumo

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def actualizar(id):
        db.session.commit()
        return True