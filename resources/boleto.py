from flask import render_template, session, redirect, url_for, flash, request
from helpers.auth import authenticated
from resources.cliente import verificarSesion
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
    print("LLEGUE AL METODO")
    new_boleto = Boleto(session["id"], id)
    new_boleto.save()
    flash("Compra exitosa", "success")
    return redirect(url_for('home_cliente')) #tendria que redireccionar al listado de proximos viajes

def cancelar_viaje(id_boleto):
    verificarSesion()
    boleto = Boleto.buscarBoletoPorId(id_boleto)
    boleto.estado = 4
    Boleto.actualizar(boleto)
    flash("Cancelacion exitosa", "success")
    return redirect(url_for('home_cliente'))
