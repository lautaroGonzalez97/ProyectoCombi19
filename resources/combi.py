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
    if (evaluarPatente(patente)):
        new_combi = Combi(patente, modelo, asientos, tipo, chofer)
        new_combi.save()
        return redirect(url_for("listado_combis"))
    else:
        #FLASH que informa que la combi ya esta cargada en el sistema    
        return redirect(url_for("render_alta_combi")) 

def devolverPatentes():
    aux = Combi.all()
    patentes=[]
    for c in aux:
        patentes.append(c.patente)
    return patentes

def evaluarPatente(patente):
    aux = devolverPatentes()
    print (aux)
    if (patente in aux):
        return False
    return True
