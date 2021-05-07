from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.combi import Combi
from models.personal import Personal
from resources.personal import verificarSesionAdmin 

def render_alta_combi():
    verificarSesionAdmin()
    personal = Personal.all()
    choferes = list (filter(lambda x: x.tipo == 2, personal))
    return render_template("addCombi.html", choferes = choferes)

def listado_combis(): 
    verificarSesionAdmin()
    combis = Combi.all()
    return render_template("listaCombis.html", combis = combis)

def alta_combi():
    datos = request.form
    patente = datos["patente"]
    modelo = datos["modelo"]
    asientos = datos["asientos"]
    tipo = datos["tipos"]
    chofer = datos["choferes"]
    new_combi = Combi(patente, modelo, asientos, tipo, chofer)
    new_combi.save()
    return redirect(url_for("listado_combis"))

def render_editar_combi(id):
    verificarSesionAdmin()
    combi = Combi.buscarCombiPorId(id)
    personal = Personal.all()
    choferes = list (filter(lambda x: x.tipo == 2, personal))
    return render_template("editCombi.html", combi = combi, choferes = choferes)

def editar_combi(id):
    combi = Combi.buscarCombiPorId(id)
    datos = request.form
    combi.patente = datos["patente"]
    combi.modelo = datos["modelo"]
    combi.tipo = datos["tipos"]
    combi.email_chofer = datos["choferes"]
    Combi.actualizar(combi)
    return redirect(url_for("listado_combis"))