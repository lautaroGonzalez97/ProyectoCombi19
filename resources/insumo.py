from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.insumo import Insumo
from resources.personal import verificarSesionAdmin 

def listado_insumos():
    verificarSesionAdmin()
    insumos = Insumo.all()
    if len(insumos) == 0:
        flash ("No hay insumos cargados", "warning")
    return render_template("listaInsumos.html", insumos = insumos)

def render_alta_insumo():
    verificarSesionAdmin()
    return render_template("addInsumo.html")

def render_editar_insumo(id):
    verificarSesionAdmin()
    insumo = Insumo.buscarInsumoPorId(id)
    return render_template("editInsumo.html", insumo = insumo)

def alta_insumo():
    insumo = request.form
    nombre = insumo["nombre"]
    tipo = insumo["tipo"]
    precio = insumo["precio"]
    new_insumo = Insumo(nombre, tipo, precio)
    new_insumo.save()
    flash ("Alta de insumo exitoso", "success")
    return redirect(url_for("listado_insumos"))

def editar_insumo(id):
    insumo = Insumo.buscarInsumoPorId(id)
    datos = request.form
    insumo.nombre = datos["nombre"]
    insumo.tipo = datos["tipo"]
    insumo.precio = datos["precio"]
    Insumo.actualizar(insumo)
    flash ("Datos del insumo actualizado exitosamente", "success")
    return redirect(url_for("listado_insumos"))

def eliminar_insumo(id):
    insumo = Insumo.buscarInsumoPorId(id)
    Insumo.eliminar_insumo(insumo)
    flash ("Baja de insumo exitoso", "success")
    return redirect(url_for("listado_insumos"))
