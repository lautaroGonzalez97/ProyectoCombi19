from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.lugar import Lugar
from resources.personal import verificarSesionAdmin 

def listado_lugares():
    verificarSesionAdmin()
    lugares = Lugar.all()
    return render_template("listaLugares.html", lugares = lugares)


def render_alta_lugar():
    verificarSesionAdmin()
    return render_template("addLugar.html")

def comprobarDatos(datos):
    localidad = datos["localidad"]
    provincia = datos["provincia"]
    lugar = Lugar.buscarPorLocalidadYProvincia(localidad, provincia)
    if (lugar is None):
        return True
    else:
        return False

def alta_lugar():
    datos = request.form
    noExiste = comprobarDatos(datos)
    if (noExiste):
        localidad = datos["localidad"]
        provincia = datos["provincia"]
        new_lugar = Lugar(localidad, provincia)
        new_lugar.save()
        return redirect(url_for("listado_lugares"))
    return redirect(url_for("render_alta_lugar"))