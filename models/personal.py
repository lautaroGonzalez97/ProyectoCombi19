from db import db

class Personal(db.Model):
    __tablename__ = 'personal'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    apellido = db.Column(db.String(255))
    email = db.Column(db.String(255))
    telefono = db.Column(db.Integer)
    password = db.Column(db.String(255))
    tipo = db.Column(db.Integer)
    combis = db.relationship('Combi', backref='combi')

    def __init__(self, nombre, apellido, email, telefono, password):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.password = password
        self.tipo = 2


    #aca van las asociaciones entre las tablas, averiguar
    def all():
        personal = Personal.query.all()
        return personal

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def actualizar(self):
        db.session.commit()
        return True

    def idPersonal(self):
        personal = self.query.filter_by(email=self.email)
        idPersonal = personal.first().id
        return idPersonal

    def tipoPersonal(self):
        personal = self.query.filter_by(email=self.email)
        tipoPersonal = personal.first().tipo
        return tipoPersonal

    def buscarEmailPassword(unEmail, unaPass):
        personal = Personal.query.filter_by(email=unEmail, password=unaPass)
        if (personal.count() == 1):
            resultado = [personal.first().idPersonal(), personal.first().tipoPersonal()]
        else:
            resultado = [None, ""]
        return resultado

    def buscarChoferPorId(id):
        chofer = Personal.query.filter_by(id=id).first()
        return chofer

    def eliminar_chofer(chofer):
        db.session.delete(chofer)
        db.session.commit()
        return True

def nombreCompleto(self):
    return self.nombre + self.apellido