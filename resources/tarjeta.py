from resources.cliente import verificarSesion
from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.tarjeta import Tarjeta
from models.cliente import Cliente
from datetime import datetime
from dateutil.relativedelta import relativedelta

def validarNumero(numero):
    if (len(numero) == 16):
        return True  
    else: return False  

def crear(nom, ape, email, nac, contra):
    datos = request.form
    nombre = datos["nombre"]
    numero = datos["numero"]
    codigo = datos["codSeguridad"]
    fechaVencimiento = datos["fechaVencimiento"]
    fechaVen = datetime.strptime(fechaVencimiento, "%Y-%m-%d")
    hoy = datetime.today() 
    if (fechaVen > hoy):
        if (validarNumero(numero)):
            cliente = Cliente(nom, ape, email, nac, contra)
            cliente.save()
            c = Cliente.buscarPorEmail(email)
            new_tarjeta = Tarjeta(nombre, numero, codigo, fechaVencimiento, c.id) #guarda en la bd cualquier cosa
            print(new_tarjeta.nombre)
            print(new_tarjeta.numero)
            new_tarjeta.save()
            print(new_tarjeta.numero)
            flash ("Registro Gold exitoso", "success")
            return redirect(url_for("login_cliente"))
        else:
            flash ("Numero de tarjeta incorrecto", "error")
            return render_template ("datosTarjeta.html", nom = nom, ape = ape, email = email, nac = nac, contra = contra)
    else:
        flash ("Tarjeta vencida", "error")
        return render_template ("datosTarjeta.html", nom = nom, ape = ape, email = email, nac = nac, contra = contra)

def eliminar_tarjeta (id):
    tarjeta= Tarjeta.buscarPorId(id)
    Tarjeta.eliminar_tarjeta(tarjeta)
    flash ("Baja de tarjeta exitoso", "success")
    return redirect (url_for("ver_perfil"))

def render_editar_tarjeta(id):
    verificarSesion()
    tarjeta=Tarjeta.buscarPorId(id)
    return render_template('editTarjeta.html', tarjeta=tarjeta)

def editar_tarjeta(id):
    tarjeta= Tarjeta.buscarPorId(id)
    datos = request.form
    fechaVen = datetime.strptime(datos["fechaVencimiento"], "%Y-%m-%d")
    hoy = datetime.today() 
    if (fechaVen > hoy):
        if (validarNumero(datos["numero"])):
            tarjeta.nombre = datos["nombre"]
            tarjeta.numero = datos["numero"]
            tarjeta.codigo = datos["codSeguridad"]
            tarjeta.fechaVencimiento = fechaVen
            Tarjeta.actualizar(tarjeta)
            flash ("Datos de tarjeta actualizados exitosamente", "success")
            return redirect(url_for("ver_perfil"))
        else:
            flash ("Numero de tarjeta incorrecto", "error")
            return redirect (url_for('render_editar_tarjeta', id = id))
    else:
        flash ("Tarjeta vencida", "error")
        return redirect (url_for('render_editar_tarjeta', id = id))

