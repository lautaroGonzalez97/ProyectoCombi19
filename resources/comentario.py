from resources.lugar import comprobarDatos
from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from resources.cliente import verificarSesion 
from models.comentario import Comentario
from models.cliente import Cliente
from datetime import  datetime,time, timedelta, date

def listado_comentarios():
    verificarSesion()
    comentarios = Comentario.all()
    comentPost=[]
    for each in comentarios:
        comentPost.append({
            'id':each.id,
            'desc': each.descripcion,
            'nomCliente': Cliente.buscarPorId(each.idCliente).nombre,
            'apeCliente': Cliente.buscarPorId(each.idCliente).apellido,
            'fecha': each.fecha
        })
    return render_template ("listaComentarios.html", comentarios = comentPost, idCliente = session["id"])

def listado_misComentarios():
    verificarSesion()
    cliente_comen = (Cliente.buscarPorId(session["id"])).comentarios
    if (len(cliente_comen) == 0):
        flash("No tienes comentarios hasta el momento", "warning")
        return render_template("listaMisComentarios.html")
    else:
        return render_template("listaMisComentarios.html", comentarios = cliente_comen)

def render_editar_comentario(id):
    verificarSesion()
    comentario = Comentario.buscarComentarioPorId(id)
    return render_template("editComentario.html", comentario = comentario)

def alta_comentario(id):
    datos = request.form
    desc = datos["descripcion"]
    fecha = date.today()
    new_comentario = Comentario(id, desc, fecha)
    Comentario.save(new_comentario)
    return redirect(url_for('listado_comentarios'))

def editar_comentario(id):
    comen = Comentario.buscarComentarioPorId(id)
    datos = request.form
    comen.descripcion = datos["descripcion"]
    comen.fecha = date.today()
    Comentario.actualizar(comen)
    flash("Comentario editado de manera exitosa")
    comentarios = (Cliente.buscarPorId(session["id"])).comentarios
    return render_template("listaMisComentarios.html", comentarios = comentarios)

def eliminar_comentario(id):
    idCliente = session["id"]
    comentario = Comentario.buscarComentarioPorId(id)
    Comentario.eliminar_comentario(comentario)
    flash("Comentario eliminado exitosamente", "success")
    comentarios = (Cliente.buscarPorId(idCliente)).comentarios
    if (len(comentarios) == 0):
        flash("No tienes comentarios hasta el momento", "warning")
        return render_template("listaMisComentarios.html")
    else:
        return render_template("listaMisComentarios.html", comentarios = comentarios)
