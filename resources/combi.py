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

def render_editar_combi(id):
    verificarSesionAdmin()
    combi = Combi.buscarCombiPorId(id)
    personal = Personal.all()
    choferes = list (filter(lambda x: x.tipo == 2, personal))
    return render_template("editCombi.html", combi = combi, choferes = choferes)

def listado_combis(): 
    verificarSesionAdmin()
    combis = Combi.all()
    if len(combis) == 0:
        flash ("No hay combis cargadas", "warning")
    return render_template("listaCombis.html", combis = combis)

def alta_combi():
    datos = request.form
    patente = datos["patente"]
    modelo = datos["modelo"]
    asientos = datos["asientos"]
    tipo = datos["tipos"]
    chofer = datos["choferes"]
    if (evaluarPatente(patente)):
        new_combi = Combi(patente, modelo, asientos, tipo, chofer)
        new_combi.save()
        flash ("Alta de combi exitoso", "success")
        return redirect(url_for("listado_combis"))
    else:
        flash ("Patente cargada en el sistema", "error")  
        return redirect(url_for("render_alta_combi")) 

def devolverPatentes():
    aux = Combi.all()
    patentes=[]
    for c in aux:
        patentes.append(c.patente)
    return patentes

def evaluarPatente(patente):
    aux = devolverPatentes()
    if (patente in aux):
        return False
    return True

def editar_combi(id):
    verificarSesionAdmin()
    combi = Combi.buscarCombiPorId(id)
    datos = request.form
    if (combi.patente != datos["patente"]):
        if (evaluarPatente(datos["patente"])):
            combi.patente = datos["patente"]
            combi.modelo = datos["modelo"]
            combi.asientos = datos["asientos"]
            combi.tipo = datos["tipos"]
            combi.id_chofer = datos["choferes"] #falta arreglar esta verificacion, no queda bien el edit cuando se edita con una patente que ya existe
            Combi.actualizar(combi)
            flash ("Datos de la combi actualizados", "success")
            return redirect(url_for("listado_combis"))
        else:
            personal = Personal.all()
            choferes = list (filter(lambda x: x.tipo == 2, personal))
            flash ("Patente cargada de sistema", "error") 
            return render_template("editCombi.html", combi = combi, choferes = choferes)
    else:
        combi.modelo = datos["modelo"]
        combi.asientos = datos["asientos"]
        combi.tipo = datos["tipos"]
        combi.id_chofer = datos["choferes"] #falta arreglar esta verificacion, no queda bien el edit cuando se edita con una patente que ya existe
        Combi.actualizar(combi)
        flash ("Datos de la combi actualizados", "success")
        return redirect(url_for("listado_combis"))
    