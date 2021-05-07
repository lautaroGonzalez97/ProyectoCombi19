from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.combi import Combi
from resources.personal import verificarSesionAdmin 

def listado_combis(): 
    verificarSesionAdmin()
    combis = Combi.all() 
    return render_template("listaCombis.html", combis = combis)