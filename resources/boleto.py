from flask import render_template, session, redirect, url_for, flash, request
from helpers.auth import authenticated
from resources.cliente import buscarViaje, verificarSesion
from models.boleto import Boleto
from models.viaje import Viaje
from models.ruta import Ruta
from models.lugar import Lugar

def render_comprar_viaje(id):
    print("ID DEL VIAJE: ")
    print(id)
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
    return render_template('cliente/comprarViaje.html', viaje = detalleViaje[0])

def comprar_viaje(id):
    verificarSesion()
    datos = request.form
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

def cancelar_viaje(id):
    verificarSesion()
    boleto = Boleto.buscarBoletoPorId(id)
    if (boleto.estado == 1):
        boleto.estado = 4
        viaje = Viaje.buscarViajePorId(boleto.id_viaje)
        viaje.asientos_disponibles += boleto.cantidad_boletos
        Viaje.actualizar(viaje) 
        Boleto.actualizar(boleto)
        flash("Cancelacion exitosa", "success")
        return redirect(url_for('ver_mis_viajes'))
    else:
        flash("No puede cancelar el boleto", "error")
        return redirect(url_for('ver_mis_viajes'))
