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
    print (nom, ape, email)
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
            new_tarjeta = Tarjeta(nombre, numero, codigo, fechaVencimiento, c.id)
            new_tarjeta.save()
            return redirect(url_for("login_cliente"))
        else:
            return render_template ("datosTarjeta.html", nom = nom, ape = ape, email = email, nac = nac, contra = contra)
    else:
        return render_template ("datosTarjeta.html", nom = nom, ape = ape, email = email, nac = nac, contra = contra)
