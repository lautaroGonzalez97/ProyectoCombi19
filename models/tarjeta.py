from db import db

class  Tarjeta (db.Model):
    __tablename__ = "terjeta_credito"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    numero = db.Column(db.Integer)
    codigo = db.Column(db.Integer)
    fechaVencimiento = db.Column(db.Date())
    id_owner = db.Column(db.Integer, db.ForeignKey('cliente.id'))

    def __init__(self, nombre, numero, codigoSeguridad, fechaVencimiento, id_owner):
        self.nombre = nombre
        self.numero = numero
        self.codigo = codigoSeguridad
        self.fechaVencimiento = fechaVencimiento
        self.id_owner = id_owner
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        return True
    
    def buscarPorId(id):
        tarjeta= Tarjeta.query.filter_by(id=id).first()
        return tarjeta

    def eliminar_tarjeta(tarjeta):
        db.session.delete(tarjeta)
        db.session.commit()
        return True

    def actualizar(self):
        db.session.commit()
        return True