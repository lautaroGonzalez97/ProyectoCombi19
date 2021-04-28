from flask import render_template, session, redirect, url_for, flash, request
from helpers.auth import authenticated

def login():
#    if (authenticated(session)):
#        return redirect(url_for("#")) #redirije a home
    return render_template("login.html")

'''def autenticar():
    datos = request.form 
    email = datos["email"]
    password = datos["password"]
    idUser = buscar usuario en la bd que coincida con email y password y me devuelve el campo id
    if (idUser is not None):
        session["id"] = idUser
    else:
        flash ("Correo o clave incorrecta", "error")
        return redirect(url_for("login")
    return redirect(url_for("#") #redirije a home

def logout():
    if(authenticated(session)):
        del session["id"]
    return redirect(url_for("login"))'''
