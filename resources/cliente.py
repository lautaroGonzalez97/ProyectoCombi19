from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.cliente import Cliente
from datetime import datetime
from dateutil.relativedelta import relativedelta

def verificarSesion():
    if (not authenticated(session) or (not session["tipo"] == "Cliente")):
        abort(401)

def home():
    verificarSesion()
    return render_template("homeCliente.html")

def login():
    if (authenticated(session)):
        return redirect(url_for("home_cliente"))
    return render_template("login_client.html")

def logOut():
    if (authenticated(session)):
        del session["id"]
    return redirect(url_for("login_cliente"))

def registrar():
    return render_template("addClient.html")

def editar():
    return render_template("editClient.html")

def comprobarDatos(data):
    resultado = [True, ""]
    email = data["email"]
    emailExiste = Cliente.buscarPorEmail(email=email)
    if(emailExiste is not None):
        resultado[0] = False
        resultado[1] = "Email ya registrado en la Base de Datos"
    return resultado

def validarPassword(password):
    if (6 < len(password) <= 16):
        return True  
    else: return False  

def crear():
    cliente = request.form
    check = comprobarDatos(cliente)
    if (check[0]):
        nombre = cliente["nombre"]
        apellido = cliente["apellido"]
        email = cliente["email"]
        fechaNacimiento = cliente["fechaNacimiento"]
        password = cliente["password"]
        fechaNac = datetime.strptime(fechaNacimiento, "%Y-%m-%d")
        fecha = fechaNac + relativedelta(years=+18)
        hoy = datetime.today() 
        if (validarPassword(password)):
            if (fecha <= hoy):
                if (request.form.get('tipo') == 'isTrue'):
                    return render_template ("datosTarjeta.html", nom = nombre, ape = apellido, email = email, nac = fechaNacimiento, contra = password)
                new_cliente = Cliente(nombre, apellido, email, fechaNac, password)  
                new_cliente.save() 
                return redirect(url_for("login_cliente"))
            else:
                return redirect(url_for("render_altaCliente"))
        else:
            return redirect(url_for("render_altaCliente"))
    else:
        return redirect(url_for("render_altaCliente"))

def autenticar():
    datos = request.form
    email = datos["email"]
    password = datos["password"]
    print(email)
    print(password)
    idClient = Cliente.buscarEmailPassword(email,password)
    print(idClient)
    if (idClient is not None):
        session["id"] = idClient
        session["tipo"] = "Cliente"
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login_cliente"))