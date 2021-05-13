from resources.lugar import comprobarDatos
from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.ruta import Ruta
from models.combi import Combi
from models.viaje import Viaje
from models.lugar import Lugar
from resources.personal import verificarSesionAdmin 

def listado_viajes():
    verificarSesionAdmin()
    viajes = Viaje.all()
    viajePost=[]
    for each in viajes:
        viajePost.append({
            'id':each.id,
            'origen': Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(each.id_ruta).id_origen).localidad,
            'destino': Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(each.id_ruta).id_destino).localidad,
            'combi': Combi.buscarCombiPorId(Ruta.buscarRutaPorId(each.id_ruta).id_combi).patente,
            'asientos': each.asientos_disponibles,
            'fecha': each.fecha,
            'precio': each.precio
        })
    if (len(viajes) == 0):
        flash ("No hay viajes cargados", "warning")
    return render_template ("listaViajes.html", viajes = viajePost)

def render_alta_viaje():
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
    return render_template("addViaje.html", rutas = rutasPost)

def alta_viaje():
    datos = request.form
    id_ruta = datos["ruta"]
    asientos = datos["asientos"]
    fecha = datos ["fecha"]
    precio = datos ["precio"]
    new_viaje= Viaje(id_ruta,asientos,fecha,precio)
    new_viaje.save()
    flash("Alta de viaje exitoso", "success")
    return redirect (url_for('listado_viajes'))

def eliminar_viaje(id):
    viaje = Viaje.buscarViajePorId(id)
    Viaje.eliminar_viaje(viaje)
    flash ("Baja de viaje exitoso", "success")
    return redirect (url_for('listado_viajes'))
