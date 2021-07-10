from db import db

class  Boleto (db.Model):
    __tablename__ = "cliente_compra_viaje"
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    id_viaje = db.Column(db.Integer, db.ForeignKey('viaje.id'))
    estado = db.Column(db.Integer) # 1=pendiente 2=en curso 3=finalizado 4=cancelado 5=rechazado 6=ausente 7=viaje eliminado 8=canceladoXchofer 9= Aceptado
    cantidad_boletos = db.Column (db.Integer)

    def __init__(self, cliente, viaje, cantidad_boletos):
        self.id_cliente = cliente
        self.id_viaje = viaje
        self.estado = 1
        self.cantidad_boletos = cantidad_boletos

    def all():
        boletos = Boleto.query.all()
        return boletos

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def actualizar (self):
        db.session.commit()
        return True

    def buscarBoletoPorId(id):
        boleto = Boleto.query.filter_by(id=id).first()
        return boleto

    def buscarBoletosParaPersonaPendiente(id):
        boletos = Boleto.query.filter_by(id_cliente=id, estado =1)
        return boletos

    def buscarBoleto():
        boletos = Boleto.query.all()
        return boletos
    
    def buscarBoletoPorCliente(id):
        boletos = Boleto.query.filter_by(id_cliente=id).first()
        return boletos

    def buscarBoletoPorIdViajeYPendiente(id):
        boletos = Boleto.query.filter_by(id_viaje=id, estado=1)
        return boletos

    def buscarBoletoPorIdViaje(id):
        boletos = Boleto.query.filter_by(id_viaje=id)
        return boletos
    
    def buscarBoletoPorIdViajeIdCliente(idv, idp):
        boleto = Boleto.query.filter_by(id_viaje=idv, id_cliente=idp).first()
        return boleto
