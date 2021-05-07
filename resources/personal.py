from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.personal import Personal

def verificarSesionChofer():
    if (not (authenticated(session)) or (not (session["tipo"] == "Chofer"))):
        abort(401)

def verificarSesionAdmin():
    if (not (authenticated(session)) or (not (session["tipo"] == "Admin"))):
        abort(401)

def home_chofer():
    verificarSesionChofer()
    return render_template("homeChofer.html")

def home_admin():
    verificarSesionAdmin()
    return render_template("homeAdmin.html")

def listado_chofer():
    verificarSesionAdmin()
    personal = Personal.all()
    choferes = list (filter(lambda x: x.tipo == 2, personal))
    return render_template("listaChoferes.html", choferes = choferes)
    
def render_alta_chofer():
    verificarSesionAdmin()
    return render_template("addChofer.html")

def render_editar_chofer(id):
    verificarSesionAdmin()
    chofer = Personal.buscarChoferPorId(id)
    return render_template("editChofer.html", chofer = chofer)

def login():
    if (authenticated(session)):
        return redirect(url_for("home_personal"))
    return render_template("login_personal.html")

def logOut():
    if (authenticated(session)):
        del session["id"]
    return redirect(url_for("login_personal"))

def listaChoferes():
    personal = Personal.all()
    choferes = list (filter(lambda x: x.tipo == 2, personal))
    return choferes

def autenticar():
    datos = request.form
    email = datos["email"]
    password = datos["password"]
    info = Personal.buscarEmailPassword(email,password)
    if (info[0] is None):
        return redirect(url_for("login_personal"))
    else:
        if (info[1] == 2):
            session["id"] = info[0] 
            session["tipo"] = "Chofer"
            return redirect(url_for("home_chofer")) 
        else:
            session["id"] = info[0]  
            session["tipo"] = "Admin"
            return redirect(url_for("home_admin"))

def validarPassword(password):
    if (6 < len(password) <= 16):
        return True  
    else: return False  

def alta_chofer():
    chofer = request.form
    nombre = chofer["nombre"]
    apellido = chofer["apellido"]
    email = chofer["email"]
    telefono = chofer["telefono"]
    password = chofer["password"]
    if (validarPassword(password)):
        new_chofer = Personal(nombre, apellido, email, telefono, password)
        new_chofer.save()
        return redirect(url_for("listado_chofer"))
    return redirect(url_for("render_alta_chofer"))

def editar_chofer(id):
    verificarSesionAdmin()
    chofer = Personal.buscarChoferPorId(id)
    datos = request.form
    chofer.nombre = datos["nombre"]
    chofer.apellido = datos["apellido"]
    chofer.email = datos["email"]
    chofer.telefono = datos["telefono"]
    chofer.password = datos["password"]
    if (validarPassword(chofer.password)):
        Personal.actualizar(chofer)
        return redirect(url_for("listado_chofer"))
    return render_template("editChofer.html", chofer = chofer)