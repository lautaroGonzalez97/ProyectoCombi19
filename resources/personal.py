from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.personal import Personal

def verificarSesion():
    if (not (authenticated(session))):
        abort(401)

def login():
    if (authenticated(session)):
        return redirect(url_for("home_personal"))
    return render_template("login_personal.html")

def logOut():
    if (authenticated(session)):
        del session["id"]
    return redirect(url_for("login_personal"))

def autenticar():
    datos = request.form
    email = datos["email"]
    password = datos["password"]
    idPersonal = Personal.buscarEmailPassword(email,password)
    if (idPersonal is None):
        return redirect(url_for("login_personal"))
    session["id"] = idPersonal
    return redirect(url_for("home_personal"))    

def home():
    verificarSesion()
    return render_template("homeChofer.html")