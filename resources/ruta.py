from resources.lugar import comprobarDatos
from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.ruta import Ruta
from models.lugar import Lugar
from models.combi import Combi
from models.viaje import Viaje
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

def render_editar_ruta(id):
    verificarSesionAdmin()
    combis = Combi.all()
    lugares = Lugar.all()
    ruta = Ruta.buscarRutaPorId(id)
    return render_template("editRuta.html", ruta = ruta, combis = combis, lugares = lugares)

def comprobarDatos(origen, destino, combi):
    ruta = Ruta.buscarRutaPorOrigenYDestinoYCombi(origen, destino, combi)
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
    if (origen != destino):
        if (comprobarDatos(origen, destino, combi)):
            new_ruta = Ruta(origen, destino, combi, duracion, km)
            new_ruta.save()
            flash("Alta de ruta exitosa", "success")
            return redirect(url_for("listado_rutas"))
        else:
            flash("Ruta cargada en el sistema", "error")
            return redirect(url_for("render_alta_ruta"))
    else: 
        flash ("Error. Origen y destino deben ser distintos","error")     # NUEVO   error, origen destino iguales
        return redirect(url_for("render_alta_ruta"))

def editar_ruta(id):
    verificarSesionAdmin()
    ruta = Ruta.buscarRutaPorId(id)
    datos = request.form
    aux1= datos["origen"]
    aux2= datos["destino"]
    if (aux1 != aux2):
        if ((int(datos["origen"]) != ruta.id_origen) or (int(datos["destino"]) != ruta.id_destino) or ((int(datos["combi"] != ruta.id_combi )))):
            if (comprobarDatos(datos["origen"], datos["destino"], int(datos["combi"]))):
                ruta.id_origen = datos['origen']
                ruta.id_destino = datos['destino']
                ruta.id_combi = datos['combi']
                ruta.duracion_minutos = datos['duracion']
                ruta.km = datos['kilometros']
                Ruta.actualizar(ruta)
                flash("Datos de ruta actualizados exitosamente", "success")
                return redirect(url_for("listado_rutas"))
            else:
                flash("Ruta cargada en el sistema", "error")
                combis = Combi.all()
                lugares = Lugar.all()
                ruta = Ruta.buscarRutaPorId(id)
                return render_template("editRuta.html", ruta = ruta, combis = combis, lugares = lugares)
        else:
            ruta.duracion_minutos = datos['duracion']
            ruta.km = datos['kilometros']
            Ruta.actualizar(ruta)
            flash("Datos de ruta actualizados exitosamente", "success")
            return redirect(url_for("listado_rutas"))
    else:
        flash ("Error. Origen y destino deben ser distintos","error")   #NUEVO   error, origen destino iguales
        combis = Combi.all()
        lugares = Lugar.all()
        ruta = Ruta.buscarRutaPorId(id)
        return render_template("editRuta.html", ruta = ruta, combis = combis, lugares = lugares)

def eliminar_ruta(id):
    ruta = Ruta.buscarRutaPorId(id)
    if not (viajesPendientes(ruta.viajes)):
        flash ("Baja de ruta exitoso", "success")
        Ruta.eliminar_ruta(ruta)
    else:
        flash ("El lugar tiene asignada al menos un viaje, por favor realice las operaciones necesarias y vuelve a intentarlo", "error")
    return redirect(url_for('listado_rutas'))

def viajesPendientes (viajes):
    index= 0
    print (len(viajes))
    if (len(viajes) != 0):
        while (index < len(viajes)):
            while (viajes[index].estado != 1) and (index < len(viajes)):
                print (index)
                index= index + 1
        if (viajes[index-1].estado == 1):
            return True
    return False        