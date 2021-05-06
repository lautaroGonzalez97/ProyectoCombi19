from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.insumo import Insumo

def verificarSesion():
    if (not (authenticated(session))):
        abort(401) 

def listado_insumos():
    verificarSesion()
    insumos = Insumo.all()
    return render_template("listaInsumos.html", insumos = insumos)

def render_alta_insumo():
    verificarSesion()
    return render_template("addInsumo.html")

def render_editar_insumo(id):
    verificarSesion()
    insumo = Insumo.buscarInsumoPorId(id)
    return render_template("editInsumo.html", insumo = insumo)

def alta_insumo():
    insumo = request.form
    nombre = insumo["nombre"]
    tipo = insumo["tipo"]
    precio = insumo["precio"]
    new_insumo = Insumo(nombre, tipo, precio)
    new_insumo.save()
    return redirect(url_for("listado_insumos"))

def editar_insumo(id):
    verificarSesion()
    insumo = Insumo.buscarInsumoPorId(id)
    datos = request.form
    insumo.nombre = datos["nombre"]
    insumo.tipo = datos["tipo"]
    insumo.precio = datos["precio"]
    Insumo.actualizar(insumo)
    return redirect(url_for("listado_insumos"))