from flask import render_template, session, redirect, url_for, flash, request
from helpers.auth import authenticated
from resources.cliente import buscarViaje, verificarSesion, esGold
from resources.tarjeta import validarNumero
from models.boleto import Boleto
from models.viaje import Viaje
from models.ruta import Ruta
from models.lugar import Lugar
from datetime import datetime
from dateutil.relativedelta import relativedelta

def render_comprar_viaje(id):
    viaje = Viaje.buscarViajePorId(id)
    detalleViaje = []
    detalleViaje.append({
        'id': id,
        'origen': Lugar.buscarLugarPorId((Ruta.buscarRutaPorId(viaje.id_ruta)).id_origen).localidad,
        'destino': Lugar.buscarLugarPorId((Ruta.buscarRutaPorId(viaje.id_ruta)).id_destino).localidad,
        'fecha': viaje.fecha,
        'salida': viaje.horaSalida,
        'llegada': viaje.horaLlegada,
        'precio': viaje.precio
    })
    gold = esGold(session["id"])
    print(gold)
    return render_template('cliente/comprarViaje.html', viaje = detalleViaje[0], esgold = gold)

def comprar_viaje(id):
    verificarSesion()
    datos = request.form
    if (not esGold(session["id"])):
        return render_template("tarjeta/pagarConTarjeta.html", id_viaje = id, boletos = datos["cantidadBoletos"])
    if (int(datos["cantidadBoletos"]) <= devolverDisponibles(id)):
        viaje= Viaje.buscarViajePorId(id)
        viaje.asientos_disponibles = viaje.asientos_disponibles - int(datos["cantidadBoletos"])
        viaje.actualizar()
        new_boleto = Boleto(session["id"], id, int(datos["cantidadBoletos"]))
        new_boleto.save()
        flash("Compra exitosa", "success")
        return redirect(url_for('ver_mis_viajes'))
    else:
        viaje = Viaje.buscarViajePorId(id)
        detalleViaje = []
        detalleViaje.append({
            'id': id,
            'origen': Lugar.buscarLugarPorId((Ruta.buscarRutaPorId(viaje.id_ruta)).id_origen).localidad,
            'destino': Lugar.buscarLugarPorId((Ruta.buscarRutaPorId(viaje.id_ruta)).id_destino).localidad,
            'fecha': viaje.fecha,
            'salida': viaje.horaSalida,
            'llegada': viaje.horaLlegada,
            'precio': viaje.precio
        })
        flash ("No contamos con esa cantidad de asientos disponibles", "error")
        return render_template('cliente/comprarViaje.html', viaje = detalleViaje[0])

def devolverDisponibles(id):
    viaje = Viaje.buscarViajePorId(id)
    print (viaje.asientos_disponibles)
    return viaje.asientos_disponibles

def pagar_con_tarjeta(id, boletos):
    datos = request.form
    nombre = datos["nombre"]
    numero = datos["numero"]
    codigo = datos["codSeguridad"]
    fechaVencimiento = datos["fechaVencimiento"]
    fechaVen = datetime.strptime(fechaVencimiento, "%Y-%m-%d")
    hoy = datetime.today() 
    if (fechaVen > hoy):
        if (validarNumero(numero)):
            if (int(boletos) <= devolverDisponibles(id)):
                viaje= Viaje.buscarViajePorId(id)
                viaje.asientos_disponibles = viaje.asientos_disponibles - int(boletos)
                viaje.actualizar()
                new_boleto = Boleto(session["id"], id, int(boletos))
                new_boleto.save()
                flash("Compra exitosa", "success")
                return redirect(url_for('ver_mis_viajes'))
            else:
                viaje = Viaje.buscarViajePorId(id)
                detalleViaje = []
                detalleViaje.append({
                    'id': id,
                    'origen': Lugar.buscarLugarPorId((Ruta.buscarRutaPorId(viaje.id_ruta)).id_origen).localidad,
                    'destino': Lugar.buscarLugarPorId((Ruta.buscarRutaPorId(viaje.id_ruta)).id_destino).localidad,
                    'fecha': viaje.fecha,
                    'salida': viaje.horaSalida,
                    'llegada': viaje.horaLlegada,
                    'precio': viaje.precio
                })
                flash ("No contamos con esa cantidad de asientos disponibles", "error")
                return render_template('cliente/comprarViaje.html', viaje = detalleViaje[0])
        else:
            flash ("Numero de tarjeta incorrecto", "error")
            return render_template ("tarjeta/pagarConTarjeta.html", id_viaje = id, boletos = boletos)
    else:
        flash ("Tarjeta vencida", "error")
        return render_template ("tarjeta/pagarConTarjeta.html", id_viaje = id, boletos = boletos)


def cancelar_viaje(id):
    verificarSesion()
    boleto = Boleto.buscarBoletoPorId(id)
    if (boleto.estado == 1):
        boleto.estado = 4
        viaje = Viaje.buscarViajePorId(boleto.id_viaje)
        viaje.asientos_disponibles += boleto.cantidad_boletos
        Viaje.actualizar(viaje) 
        Boleto.actualizar(boleto)
        if verificarReembolso(viaje.id):
            flash ("Se le reembolsara el 100 % del pasaje", "warning")
        else:
            flash ("Se le reembolsara el 50 % del pasaje", "warning")
        flash("Cancelacion exitosa", "success")
        return redirect(url_for('ver_mis_viajes'))
    else:
        flash("No puede cancelar el boleto", "error") # NUNCA LLEGA PORQUE EN HTML BLOQUEA EL BOTON 
        return redirect(url_for('ver_mis_viajes'))

def verificarReembolso(id):
    fechaViaje = datetime.strptime(str(Viaje.buscarViajePorId(id).fecha), "%Y-%m-%d")
    hoy = datetime.today() + relativedelta(days=+2)
    if(hoy >= fechaViaje):
        return False
    else:
        return True