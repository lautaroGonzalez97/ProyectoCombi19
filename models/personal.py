from db import db

class Personal(db.Model):
    __tablename__ = 'personal'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    apellido = db.Column(db.String(255))
    email = db.Column(db.String(255))
    telefono = db.Column(db.Integer)
    password = db.Column(db.String(255))

    def __init__(self, nombre, apellido, email, telefono, password):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.password = password


    #aca van las asociaciones entre las tablas, averiguar

    def idUsuario(self):
        personal = self.query.filter_by(email=self.email)
        idPersonal = personal.first().id
        return idPersonal

    def buscarEmailPassword(unEmail, unaPass):
        personal = Personal.query.filter_by(email=unEmail, password=unaPass)
        if (personal.count() == 1):
            return personal.first().idUsuario()
        else:
            return None