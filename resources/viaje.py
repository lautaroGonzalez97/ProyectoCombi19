from resources.lugar import comprobarDatos
from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.ruta import Ruta
from models.combi import Combi
from models.viaje import Viaje
from models.lugar import Lugar
from models.personal import Personal
from resources.personal import verificarSesionAdmin 
from datetime import  datetime,time, timedelta, date

def listado_viajes():
    verificarSesionAdmin()
    viajes = Viaje.all()
    estados=["PENDIENTE","EN CURSO","CANCELADO","RECHAZADO","REALIZADO"]
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
            'horaLlegada': each.horaLlegada,
            'precio': each.precio,
            'estado':estados[each.estado - 1]
        })
    if (len(viajes) == 0):
        flash ("No hay viajes cargados", "warning")
    return render_template ("viaje/listaViajes.html", viajes = viajePost)

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
    return render_template("viaje/addViaje.html", rutas = rutasPost)

def alta_viaje():
    datos = request.form
    id_ruta = datos["ruta"]
    asientos = datos["asientos"]
    fecha = datos ["fecha"]
    precio = datos ["precio"]
    horaSalida = datos["horaSalida"]
    salida = datetime.strptime(horaSalida, "%H:%M")
    horaLlegada = sumarHora(salida, id_ruta)
    estado = 1 
    diaActual = datetime.today()
    fec = datetime.strptime(fecha, "%Y-%m-%d")
    if (fec >= diaActual):
        if (comprobar_asientos(id_ruta,asientos)):
            if (comprobarViaje(fec, horaLlegada, salida,(Combi.buscarCombiPorId(Ruta.buscarRutaPorId(id_ruta).id_combi)))):
                new_viaje= Viaje(id_ruta,asientos,fecha,salida,horaLlegada,precio,estado)
                new_viaje.save()
                flash("Alta de viaje exitoso", "success")
                return redirect (url_for('listado_viajes'))
            else:
                flash ("UPS! Este viaje es imposible realizarlo", "error")
                return redirect (url_for('render_alta_viaje'))
        else: 
            flash ("Cantidad de asientos invalida","error")
            return redirect (url_for('render_alta_viaje'))          #NUEVO   error, el num de asientos cargados es mayor a la cant de asientos de combi
    else:
        flash("Fecha invalida","error")    #NUEVO    error, la fecha cargada no supera la fecha actual
        return redirect (url_for('render_alta_viaje'))

def comprobarViaje(fec, horaLlegada, horaSalida, combi):
    viajes = Viaje.all()
    for viaje in viajes:
        if (datetime.strptime(str(viaje.fecha),"%Y-%m-%d") == fec):
            print("ES MISMA FECHA")
            if (combi.id == Ruta.buscarRutaPorId(viaje.id_ruta).id_combi) or Combi.buscarCombiPorId(Ruta.buscarRutaPorId(viaje.id_ruta).id_combi).id_chofer == combi.id_chofer:
                if (horaSalida.time() == datetime.strptime((str(viaje.horaSalida)), "%H:%M:%S").time()):
                    # flash("HORA DE SALIDA IGUAL A HORA DE SALIDA DE OTRO VIAJE PARA ESE CHOFER", "error")
                    return False
                if (horaSalida.time() > datetime.strptime((str(viaje.horaSalida)), "%H:%M:%S").time() and horaSalida.time() < datetime.strptime((str(viaje.horaLlegada)), "%H:%M:%S").time()):
                    # flash("HORA DE SALIDA ENTRE HORA DE SALIDA Y HORA DE LLEGADA DE OTRO VIAJE PARA ESE CHOFER", "error")
                    return False
                if (horaSalida.time() == datetime.strptime((str(viaje.horaLlegada)), "%H:%M:%S").time()):
                    # flash("HORA DE SALIDA IGUAL A HORA DE LLEGADA DE OTRO VIAJE PARA ESE CHOFER", "error")
                    return False
                if (horaLlegada.time() == datetime.strptime((str(viaje.horaSalida)), "%H:%M:%S").time()):
                    # flash("HORA DE LLEGADA IGUAL A HORA DE SALIDA DE OTRO VIAJE PARA ESE CHOFER", "error")
                    return False
                if (horaLlegada.time() > datetime.strptime((str(viaje.horaSalida)), "%H:%M:%S").time() and horaLlegada.time() < datetime.strptime((str(viaje.horaLlegada)), "%H:%M:%S").time()):
                    # flash("HORA DE LLEGADA ENTRE HORA DE SALIDA Y HORA DE LLEGADA DE OTRO VIAJE PARA ESE CHOFER", "error")
                    return False
                if (horaLlegada.time() == datetime.strptime((str(viaje.horaLlegada)), "%H:%M:%S").time()):    
                    # flash("HORA DE LLEGADA IGUAL A HORA DE LLEGADA DE OTRO VIAJE", "error")                 
                    return False
    return True

def sumarHora(salida, id_ruta):
    horas = int(Ruta.buscarRutaPorId(id_ruta).duracion_minutos) / 60
    minutos = int(Ruta.buscarRutaPorId(id_ruta).duracion_minutos) % 60
    dh = timedelta(hours=horas)
    dm = timedelta(minutes=minutos)
    return salida + dh + dm

def eliminar_viaje(id):
    viaje = Viaje.buscarViajePorId(id)
    if (viaje.estado == 3):                        #SE ELIMINARIA SOLO SI SE ENCUENTRA CANCELADO
        Viaje.eliminar_viaje(viaje)
        flash ("Baja de viaje exitoso", "success")
        return redirect (url_for('listado_viajes'))
    if (viaje.estado == 2):
        flash("El viaje se encuentra en curso","error")
        return redirect (url_for('listado_viajes'))
    if (viaje.estado == 1):
        flash("El viaje se encuentra pendiente","error")
        return redirect (url_for('listado_viajes'))


def comprobar_asientos(id_ruta, asientos):
    """ Comprobamos que el numero de asientos cargado no sea mayor que el numero de asientos de la combi """
    aux = Combi.buscarCombiPorId(Ruta.buscarRutaPorId(id_ruta).id_combi).asientos
    if (int(asientos) > int(aux)):
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


