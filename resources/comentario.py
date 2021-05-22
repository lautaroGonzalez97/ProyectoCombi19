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
            'apeCliente': Cliente.buscarPorId(each.idCliente).apellido
        })
    id = session["id"]
    return render_template ("listaComentarios.html", comentarios = comentPost , idCliente = id)

def alta_comentario(id):
    datos = request.form
    desc = datos["descripcion"]
    new_comentario = Comentario(session['id'], desc)
    Comentario.save(new_comentario)
    return redirect(url_for('listado_comentarios'))
