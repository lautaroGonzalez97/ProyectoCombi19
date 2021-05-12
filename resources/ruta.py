from resources.lugar import comprobarDatos
from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.ruta import Ruta
from models.lugar import Lugar
from models.combi import Combi
from resources.personal import verificarSesionAdmin 

def listado_rutas():
    verificarSesionAdmin()
    rutas = Ruta.all()
    rutasPost=[]
    for each in rutas:
        rutasPost.append({
            'id':each.id,
            'origen': Lugar.buscarLugarPorId(each.id_origen).localidad,
            'destino': Lugar.buscarLugarPorId(each.id_destino).localidad,
            'combi': Combi.buscarCombiPorId(each.id_combi).patente,
            'duracion':each.duracion_minutos,
            'km': each.km
        })
    if len(rutas) == 0:
        flash ("No hay rutas cargadas", "warning")
    return render_template("listaRutas.html", rutas = rutasPost)

def render_alta_ruta():
    verificarSesionAdmin()
    combis = Combi.all()
    lugares = Lugar.all()
    return render_template("addRuta.html", combis = combis, lugares = lugares)

def comprobarDatos(origen, destino):
    ruta = Ruta.buscarRutaPorOrigenYDestino(origen, destino)
    if (ruta is None):
        return True
    else:
        return False

def alta_ruta():
    datos = request.form
    origen = datos['origen']
    destino = datos['destino']
    combi = datos['combi']
    duracion = datos['duracion']
    km = datos['kilometros']
    if (comprobarDatos(origen, destino)):
        new_ruta = Ruta(origen, destino, combi, duracion, km)
        new_ruta.save()
        flash("Alta de ruta exitosa", "success")
        return redirect(url_for("listado_rutas"))
    else:
        flash("Ruta cargada en el sistema", "error")
        return redirect(url_for("render_alta_ruta"))