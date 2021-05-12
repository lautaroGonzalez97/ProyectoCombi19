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
    lugares=['Buenos Aires','Catamarca','Chaco','Chubut','Cordoba','Corrientes','Entre Rios','Formosa','Jujuy','La Pampa','La Rioja','Mendoza','Misiones','Neuquen','Rio Negro','Salta','San Juan','San Luis','Santa Cruz','Santa Fe','Santiago del Estero', 'Tierra del Fuego','Tucuman']    
    return render_template("addLugar.html",provincias=lugares)

def render_editar_lugar(id):
    verificarSesionAdmin()
    lugar = Lugar.buscarLugarPorId(id)
    lugares=['Buenos Aires','Catamarca','Chaco','Chubut','Cordoba','Corrientes','Entre Rios','Formosa','Jujuy','La Pampa','La Rioja','Mendoza','Misiones','Neuquen','Rio Negro','Salta','San Juan','San Luis','Santa Cruz','Santa Fe','Santiago del Estero', 'Tierra del Fuego','Tucuman']
    return render_template("editLugar.html", lugar = lugar, provincias=lugares)

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
    print((datos["localidad"] != lugar.localidad))
    if ((datos["localidad"] != lugar.localidad) or (datos["provincia"] != lugar.provincia)):
        if (comprobarDatos(datos)):
            lugar.localidad = datos["localidad"]
            lugar.provincia = datos["provincia"]
            Lugar.actualizar(lugar)
            flash ("Datos de lugar actualizados exitosamente", "success")
            return redirect(url_for("listado_lugares"))
        flash ("Lugar cargado en el sistema", "error")
        lugares=['Buenos Aires','Catamarca','Chaco','Chubut','Cordoba','Corrientes','Entre Rios','Formosa','Jujuy','La Pampa','La Rioja','Mendoza','Misiones','Neuquen','Rio Negro','Salta','San Juan','San Luis','Santa Cruz','Santa Fe','Santiago del Estero', 'Tierra del Fuego','Tucuman']
        return render_template("editLugar.html", lugar = lugar, provincias = lugares)
    else:
        lugar.localidad = datos["localidad"]
        lugar.provincia = datos["provincia"]
        Lugar.actualizar(lugar)
        flash ("Datos de lugar actualizados exitosamente", "success")
        return redirect(url_for("listado_lugares"))
    