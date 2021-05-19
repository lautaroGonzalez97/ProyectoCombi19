from resources.lugar import comprobarDatos
from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.ruta import Ruta
from models.combi import Combi
from models.viaje import Viaje
from models.lugar import Lugar
from resources.personal import verificarSesionAdmin 
from datetime import date

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
            'horaSalida': each.horaSalida,
            #'horaLlegada': #calcular la hora con la de ruta
            'precio': each.precio,
            'estado':each.estado
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
    estado = datos ["estado"]
    diaActual = datetime.now()
    if (fecha >= diaActual):
        if (comprobar_asientos(id_ruta,asientos)):
            new_viaje= Viaje(id_ruta,asientos,fecha,precio)
            new_viaje.save()
            flash("Alta de viaje exitoso", "success")
            return redirect (url_for('listado_viajes'))
        else: 
            flash ("Error de alta de viaje. Mala carga de asientos","error")
            return redirect (url_for('render_alta_viaje'))          #NUEVO   error, el num de asientos cargados es mayor a la cant de asientos de combi
    else:
        flash("Error de alta de viaje, fecha invalida","error")    #NUEVO    error, la fecha cargada no supera la fecha actual
        return redirect (url_for('render_alta_viaje'))

def eliminar_viaje(id):
    viaje = Viaje.buscarViajePorId(id)
    if (viaje.estado == 3):                        #SE ELIMINARIA SOLO SI SE ENCUENTRA CANCELADO
        Viaje.eliminar_viaje(viaje)
        flash ("Baja de viaje exitoso", "success")
        return redirect (url_for('listado_viajes'))
    if (viaje.estado == 2):
        flash("Error. El viaje se encuentra en curso","error")
        return redirect (url_for('listado_viajes'))
    if (viaje.estado == 1):
        flash("Error. El viaje se encuentra pendiente","error")
        return redirect (url_for('listado_viajes'))


def comprobar_asientos(id, asientos):
    """ Comprobamos que el numero de asientos cargado no sea mayor que el numero de asientos de la combi """
    aux = Ruta.buscarRutaPorId(id)
    if (asientos > aux.asientos):
        return False
    else:
        return True


### NO SE QUE ONDA
def devolverIdDeCombi(id):
    ruta= Ruta.buscarRutaPorId(id)
    return ruta.combi


def trabajaCombi (idRuta, idCombi):
    if (devolverIdDeCombi(idRuta) == idCombi ):
        return True
    else:
        return False


