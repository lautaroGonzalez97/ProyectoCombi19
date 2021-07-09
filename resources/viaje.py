from flask import render_template, redirect, url_for, flash, request
from models.ruta import Ruta
from models.combi import Combi
from models.viaje import Viaje
from models.lugar import Lugar
from models.boleto import Boleto
from models.cliente import Cliente
from resources.personal import verificarSesionAdmin, verificarSesionChofer 
from datetime import  datetime, timedelta
import smtplib

def listado_viajes():
    verificarSesionAdmin()
    viajes = Viaje.all()
    estados=["PENDIENTE","EN CURSO","FINALIZADO", "CANCELADO"]
    viajePost=[]
    for each in viajes:
        if (each.enabled == 1):
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
    if (len(viajePost) == 0):
        flash ("No hay viajes cargados", "warning")
    return render_template ("viaje/listaViajes.html", viajes = viajePost)

def render_alta_viaje():
    verificarSesionAdmin()
    rutas = Ruta.all()
    rutasPost=[]
    for each in rutas:
        if (each.enabled == 1):
            rutasPost.append({
                'id':each.id,
                'origen': Lugar.buscarLugarPorId(each.id_origen).localidad,
                'destino': Lugar.buscarLugarPorId(each.id_destino).localidad,
                'combi': Combi.buscarCombiPorId(each.id_combi).patente,
                'duracion':each.duracion_minutos,
                'km': each.km
            })
    return render_template("viaje/addViaje.html", rutas = rutasPost)

def render_editar_viaje(id):
    verificarSesionAdmin()
    viaje = Viaje.buscarViajePorId(id)
    rutas = Ruta.all()
    rutasPost=[]
    for each in rutas:
        if (each.enabled == 1):
            rutasPost.append({
                'id':each.id,
                'origen': Lugar.buscarLugarPorId(each.id_origen).localidad,
                'destino': Lugar.buscarLugarPorId(each.id_destino).localidad,
                'combi': Combi.buscarCombiPorId(each.id_combi).patente,
                'duracion':each.duracion_minutos,
                'km': each.km
            })
    return render_template("viaje/editViaje.html", rutas = rutasPost, viaje = viaje)

def comprobarViaje(fec, horaLlegada, horaSalida, combi):
    viajes = Viaje.all()
    for viaje in viajes:
        if (viaje.enabled == 1):
            if (datetime.strptime(str(viaje.fecha),"%Y-%m-%d") == fec):
                print("ES MISMA FECHA")
                if (combi.id == Ruta.buscarRutaPorId(viaje.id_ruta).id_combi) or Combi.buscarCombiPorId(Ruta.buscarRutaPorId(viaje.id_ruta).id_combi).id_chofer == combi.id_chofer:
                    if (horaSalida.time() == datetime.strptime((str(viaje.horaSalida)), "%H:%M:%S").time()):
                        flash("No se encuentra disponible el horario de salida ingresado para el viaje", "error")
                        return False
                    if (horaSalida.time() > datetime.strptime((str(viaje.horaSalida)), "%H:%M:%S").time() and horaSalida.time() < datetime.strptime((str(viaje.horaLlegada)), "%H:%M:%S").time()):
                        flash("No se encuentra disponible el horario de salida ingresado para el viaje", "error")
                        return False
                    if (horaSalida.time() == datetime.strptime((str(viaje.horaLlegada)), "%H:%M:%S").time()):
                        flash("No se encuentra disponible el horario de salida ingresado para el viaje", "error")
                        return False
                    if (horaLlegada.time() == datetime.strptime((str(viaje.horaSalida)), "%H:%M:%S").time()):
                        flash("No se encuentra disponible el horario de llegada ingresado para el viaje", "error")
                        return False
                    if (horaLlegada.time() > datetime.strptime((str(viaje.horaSalida)), "%H:%M:%S").time() and horaLlegada.time() < datetime.strptime((str(viaje.horaLlegada)), "%H:%M:%S").time()):
                        flash("No se encuentra disponible el horario de llegada ingresado para el viaje", "error")
                        return False
                    if (horaLlegada.time() == datetime.strptime((str(viaje.horaLlegada)), "%H:%M:%S").time()):    
                        flash("No se encuentra disponible el horario de llegada ingresado para el viaje", "error")                 
                        return False       
    return True

def comprobarViajeEDICION(fec, horaLlegada, horaSalida, combi,id):
    viajes = Viaje.all()
    for viaje in viajes:
        if ( int(viaje.id) != int(id)):
            if (viaje.enabled == 1):
                if (datetime.strptime(str(viaje.fecha),"%Y-%m-%d") == fec):
                    if (combi.id == Ruta.buscarRutaPorId(viaje.id_ruta).id_combi) or Combi.buscarCombiPorId(Ruta.buscarRutaPorId(viaje.id_ruta).id_combi).id_chofer == combi.id_chofer:
                        if (horaSalida.time() == datetime.strptime((str(viaje.horaSalida)), "%H:%M:%S").time()):
                            flash("No se encuentra disponible el horario de salida ingresado para el viaje", "error")
                            return False
                        if (horaSalida.time() > datetime.strptime((str(viaje.horaSalida)), "%H:%M:%S").time() and horaSalida.time() < datetime.strptime((str(viaje.horaLlegada)), "%H:%M:%S").time()):
                            flash("No se encuentra disponible el horario de salida ingresado para el viaje", "error")
                            return False
                        if (horaSalida.time() == datetime.strptime((str(viaje.horaLlegada)), "%H:%M:%S").time()):
                            flash("No se encuentra disponible el horario de salida ingresado para el viaje", "error")
                            return False
                        if (horaLlegada.time() == datetime.strptime((str(viaje.horaSalida)), "%H:%M:%S").time()):
                            flash("No se encuentra disponible el horario de llegada ingresado para el viaje", "error")
                            return False
                        if (horaLlegada.time() > datetime.strptime((str(viaje.horaSalida)), "%H:%M:%S").time() and horaLlegada.time() < datetime.strptime((str(viaje.horaLlegada)), "%H:%M:%S").time()):
                            flash("No se encuentra disponible el horario de llegada ingresado para el viaje", "error")
                            return False
                        if (horaLlegada.time() == datetime.strptime((str(viaje.horaLlegada)), "%H:%M:%S").time()):    
                            flash("No se encuentra disponible el horario de llegada ingresado para el viaje", "error")                 
                            return False                    
    return True

def sumarHora(salida, id_ruta):
    horas = int(Ruta.buscarRutaPorId(id_ruta).duracion_minutos) / 60
    minutos = int(Ruta.buscarRutaPorId(id_ruta).duracion_minutos) % 60
    dh = timedelta(hours=horas)
    dm = timedelta(minutes=minutos)
    return salida + dh + dm

def comprobar_asientos(id_ruta, asientos):
    #Comprobamos que el numero de asientos cargado no sea mayor que el numero de asientos de la combi
    aux = Combi.buscarCombiPorId(Ruta.buscarRutaPorId(id_ruta).id_combi).asientos
    if (int(asientos) > int(aux)):
        return False
    else:
        return True

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
    if (fec > diaActual):
        if (comprobar_asientos(id_ruta,asientos)):
            if (comprobarViaje(fec, horaLlegada, salida,(Combi.buscarCombiPorId(Ruta.buscarRutaPorId(id_ruta).id_combi)))):
                new_viaje= Viaje(id_ruta,asientos,fecha,salida,horaLlegada,precio,estado)
                new_viaje.save()
                flash("Alta de viaje exitoso", "success")
                return redirect (url_for('listado_viajes'))
            else:
                return redirect (url_for('render_alta_viaje'))
        else: 
            flash ("Cantidad de asientos invalida","error")
            return redirect (url_for('render_alta_viaje'))   
    else:
        flash("Fecha invalida","error") 
        return redirect (url_for('render_alta_viaje'))

def editar_viaje(id):
    verificarSesionAdmin()
    viaje = Viaje.buscarViajePorId(id)
    datos = request.form
    horaSalida = datos["horaSalida"]
    salida = datetime.strptime(horaSalida, "%H:%M:%S")
    aux = str(viaje.horaSalida)
    viaje_horaSalida = datetime.strptime(aux, "%H:%M:%S")
    fecha = datetime.strptime(datos['fecha'], "%Y-%m-%d")
    viaje_fecha = datetime.strptime((str(viaje.fecha)), "%Y-%m-%d")
    if (fecha != viaje_fecha) or (salida != viaje_horaSalida) or (int(datos["ruta"]) != viaje.id_ruta) :
        hoy = datetime.today()
        if (fecha > hoy):
            if (comprobar_asientos(datos["ruta"], datos["asientos"])):
                llegada = sumarHora(salida, datos["ruta"])
                if (comprobarViajeEDICION(fecha, llegada, salida, (Combi.buscarCombiPorId(Ruta.buscarRutaPorId(datos["ruta"]).id_combi)),id)):
                    viaje.id_ruta = datos["ruta"]
                    viaje.asientos_disponibles = datos["asientos"]
                    viaje.fecha = fecha
                    viaje.horaSalida = salida
                    viaje.horaLlegada = llegada
                    viaje.precio = datos["precio"]
                    Viaje.actualizar(viaje)
                    flash("Datos de viaje actulizados exitosamente", "success")
                    return redirect(url_for("listado_viajes"))
            else:
                flash ("Cantidad de asientos invalida","error")
        else:
            flash("Fecha invalida","error") 
        viaje = Viaje.buscarViajePorId(id)
        rutas = Ruta.all()
        rutasPost=[]
        for each in rutas:
            if (each.enabled == 1):
                rutasPost.append({
                    'id':each.id,
                    'origen': Lugar.buscarLugarPorId(each.id_origen).localidad,
                    'destino': Lugar.buscarLugarPorId(each.id_destino).localidad,
                    'combi': Combi.buscarCombiPorId(each.id_combi).patente,
                    'duracion':each.duracion_minutos,
                    'km': each.km
                })   
        return render_template("viaje/editViaje.html", rutas = rutasPost, viaje = viaje)
    else:
        if (viaje.asientos_disponibles != int(datos["asientos"])): 
            if (comprobar_asientos(datos["ruta"], datos["asientos"])):
                viaje.asientos_disponibles = datos['asientos']
                viaje.precio = datos["precio"]
                Viaje.actualizar(viaje)
                flash("Datos de viaje actualizados exitosamente", "success")
                return redirect(url_for("listado_viajes")) 
            else:
                flash("Cantidad de asientos invalida", "error")
                viaje = Viaje.buscarViajePorId(id)
                rutas = Ruta.all()
                rutasPost=[]
                for each in rutas:
                    if (each.enabled == 1):
                        rutasPost.append({
                            'id':each.id,
                            'origen': Lugar.buscarLugarPorId(each.id_origen).localidad,
                            'destino': Lugar.buscarLugarPorId(each.id_destino).localidad,
                            'combi': Combi.buscarCombiPorId(each.id_combi).patente,
                            'duracion':each.duracion_minutos,
                            'km': each.km
                        })   
                return render_template("viaje/editViaje.html", rutas = rutasPost, viaje = viaje) 
        else:
            viaje.precio = datos["precio"]
            Viaje.actualizar(viaje)
            flash("Datos de viaje actulizados exitosamente", "success")
            return redirect(url_for("listado_viajes")) 

def eliminar_viaje(id):
    viaje = Viaje.buscarViajePorId(id)
    if (viaje.estado == 1): 
        cancelarBoletos(viaje.id)                      
        viaje.enabled = 0
        Viaje.actualizar(viaje)
        if (viaje.asientos_disponibles != viaje.asientos):
            flash("Baja de viaje exitoso", "success")
            flash("El viaje tenia pasajes vendidos, generar reembolso a clientes", "warning")
        else:
            flash("Baja de viaje exitoso", "success")
            flash("El viaje no tenia pasajes vendidos", "warning")
        return redirect (url_for('listado_viajes'))
    if (viaje.estado == 3):
        cancelarBoletos(viaje.id)
        viaje.enabled = 0
        Viaje.actualizar(viaje)
        flash ("Baja de viaje exitoso", "success")
        return redirect (url_for('listado_viajes'))
    if (viaje.estado == 2):
        flash("El viaje se encuentra en curso","error")
        return redirect (url_for('listado_viajes'))

def cancelarBoletos(idV):
    boletos = Boleto.buscarBoleto()
    for each in boletos:
        if (each.id_viaje == idV):
            each.estado = 7
            each.actualizar()

def chofer_cancelaViaje(id):
    verificarSesionChofer()
    viaje = Viaje.buscarViajePorId(id)
    viaje.estado = 4
    Viaje.actualizar(viaje)
    boletos = Boleto.buscarBoletoPorIdViaje(id) 
    for boleto in boletos:
        if (boleto.estado == 1):
            boleto.estado = 8
            Boleto.actualizar(boleto)
            origen = Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(viaje.id_ruta).id_origen).localidad
            destino = Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(viaje.id_ruta).id_destino).localidad
            cliente = Cliente.buscarPorId(boleto.id_cliente)
            message = "Por motivos personales del chofer el viaje con origen {} y destino {} para la fecha {} ha sido cancelado. Comunicarse con nosotros para reembolso del dinero. Muchas Gracias por su tiempo".format(origen, destino, viaje.fecha)
            subject = "Cancelacion Viaje"
            message = 'Subject: {}\n\n{}'.format(subject, message)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('contacto.combi19@gmail.com', 'somoscombi19')
            server.sendmail('contacto.combi19@gmail.com', cliente.email, message)
            server.quit()
    flash("Cancelacion exitosa", "success")
    return redirect(url_for("render_viajesPendientes_chofer"))

def verListadoPasajeros(id):
    verificarSesionChofer()
    vendidos = Boleto.buscarBoletoPorIdViaje(id)
    pasajeroPost = []
    for vendido in vendidos:
        if (vendido.estado != 4):
            pasajeroPost.append({
                "id": vendido.id_cliente,
                "nombre": Cliente.buscarPorId(vendido.id_cliente).nombre,
                "apellido": Cliente.buscarPorId(vendido.id_cliente).apellido,
                "email": Cliente.buscarPorId(vendido.id_cliente).email,
                "estado": vendido.estado   
            })
    return render_template("personal/listaPasajeros.html", pasajeros = pasajeroPost, idv = id)

def comenzarViaje(id):
    verificarSesionChofer()
    viaje = Viaje.buscarViajePorId(id)
    boletos = Boleto.buscarBoletoPorIdViaje(id)
    for each in boletos:
        if each.estado == 1:
            each.estado = 2
            each.actualizar()
    viaje.estado = 2
    viaje.actualizar()
    return redirect(url_for('render_viajesPendientes_chofer'))

def finalizarViaje(id):
    verificarSesionChofer()
    viaje = Viaje.buscarViajePorId(id)
    boletos = Boleto.buscarBoletoPorIdViaje(id)
    for each in boletos:
        if each.estado == 2:
            each.estado = 3
            each.actualizar()
    viaje.estado = 3
    viaje.actualizar()
    return redirect(url_for('render_viajesFinalizados_chofer'))
    
