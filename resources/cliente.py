from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.cliente import Cliente
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import  datetime,time, timedelta, date

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
                flash ("Registro exitoso", "success")
                return redirect(url_for("login_cliente"))
            else:
                flash ("Edad invalida", "error")
                return redirect(url_for("render_altaCliente"))
        else:
            flash ("Contraseña corta", "error")
            return redirect(url_for("render_altaCliente"))
    else:
        flash ("Email registrado en el sistema", "error")
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
    flash ("Email o contraseña incorrecta", "error")
    return redirect(url_for("login_cliente"))

def ver_perfil():
    verificarSesion()
    perfil= Cliente.buscarPorId(session["id"])
    perfil.fechaNacimiento = datetime.strptime(str(perfil.fechaNacimiento),"%Y-%m-%d").date()
    if (esGold(perfil.id)):
        tarjetasPost=[]
        for each in perfil.tarjetas:
            tarjetasPost.append({
            'id':each.id,
            'nombre': each.nombre,
            'numero': each.numero,
            'codigo': each.codigo,
            'fechaVencimiento':datetime.strptime(str(each.fechaVencimiento),"%Y-%m-%d").date()
        })
        return render_template ("verPerfilGold.html", usuario= perfil, tarjetas= tarjetasPost)
    return render_template ("verPerfil.html", usuario=perfil)


def esGold (id):
        usuario = Cliente.buscarPorId(id)
        if ( len(usuario.tarjetas) != 0 ):
            return True
        return False

def render_editar_cliente (id):
    verificarSesion()
    cliente = Cliente.buscarPorId(id)
    return render_template("editClient.html", cliente = cliente)

def editar_cliente(id):
    verificarSesion()
    cliente = Cliente.buscarPorId(id)
    datos = request.form
    if (datos["email"]  != cliente.email):
        check = comprobarDatos(datos)
        if (check[0]):
            if (validarPassword(datos["password"])):
                fechaNac = datetime.strptime(datos["fechaNacimiento"], "%Y-%m-%d")
                fecha = fechaNac + relativedelta(years=+18)
                hoy = datetime.today() 
                if (fecha <= hoy):
                    cliente.nombre = datos["nombre"]
                    cliente.apellido = datos["apellido"]
                    cliente.email = datos["email"]
                    cliente.password = datos["password"]
                    cliente.fecha = fecha
                    Cliente.actualizar(cliente)
                    flash ("Datos personales actualizados exitosamente", "success")
                    return redirect(url_for ("ver_perfil"))
                else:
                    flash ("Edad invalida", "error")
                    return redirect (url_for("render_editar_cliente", id = id))
            else:
                flash ("Contraseña corta", "error")
                return redirect (url_for("render_editar_cliente", id = id))
        else:
            flash ("Email registrado en el sistema", "error")
            return redirect (url_for("render_editar_cliente", id = id))
    else:
        if (validarPassword(datos["password"])):
            fechaNac = datetime.strptime(datos["fechaNacimiento"], "%Y-%m-%d")
            fecha = fechaNac + relativedelta(years=+18)
            hoy = datetime.today() 
            if (fecha <= hoy):
                cliente.nombre = datos["nombre"]
                cliente.apellido = datos["apellido"]
                cliente.email = datos["email"]
                cliente.password = datos["password"]
                cliente.fecha = fecha
                Cliente.actualizar(cliente)
                flash ("Datos personales actualizados exitosamente", "success")
                return redirect(url_for ("ver_perfil"))
            else:
                flash ("Edad invalida", "error")
                return redirect (url_for("render_editar_cliente", id = id))
        else:
            flash ("Contraseña corta", "error")
            return redirect (url_for("render_editar_cliente", id = id))
