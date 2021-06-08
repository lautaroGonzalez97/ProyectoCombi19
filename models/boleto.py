from db import db

'''class  Boleto (db.Model):
    __tablename__ = "cliente_compra_viaje"
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    id_viaje = db.Column(db.Integer, db.ForeignKey('viaje.id'))
    estado = db.Column(db.Integer) # 1=pendiente 2=en curso 3=finalizado 4=cancelado 5=rechazado

    def __init__(self, cliente, viaje):
        self.id_cliente = cliente
        self.id_viaje = viaje
        self.estado = 1'''