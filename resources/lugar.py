from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.lugar import Lugar
from resources.personal import verificarSesionAdmin 

def listado_lugares():
    verificarSesionAdmin()
    lugares = Lugar.all()
    if len(lugares) == 0:    
        flash ("No hay lugares cargados", "warning")
    return render_template("listaLugares.html", lugares = lugares)


def render_alta_lugar():
    verificarSesionAdmin()
    return render_template("addLugar.html")

def render_editar_lugar(id):
    verificarSesionAdmin()
    lugar = Lugar.buscarLugarPorId(id)
    print(lugar.localidad)
    return render_template("editLugar.html", lugar = lugar)

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
        flash ("Alta de lugar exitoso", "success")
        return redirect(url_for("listado_lugares"))
    flash ("Lugar cargado en el sistema", "error")
    return redirect(url_for("render_alta_lugar"))

def editar_lugar(id):
    verificarSesionAdmin()
    lugar = Lugar.buscarLugarPorId(id)
    datos = request.form
    if (comprobarDatos(datos)):
        lugar.localidad = datos["localidad"]
        lugar.provincia = datos["provincia"]
        Lugar.actualizar(id)
        flash ("Datos de lugar actualizados exitosamente", "success")
        return redirect(url_for("listado_lugares"))
    flash ("Lugar cargado en el sistema", "error")
    return render_template("editLugar.html", lugar = lugar)