from flask import render_template, session, redirect, url_for, flash, request
from helpers.auth import authenticated

def render_login_client():
    return render_template("login_client.html")

def render_register_client():
    return render_template('register.html')

def render_home():
    if (authenticated(session)):
        return render_template('home.html') # render_template ('', es_chofer=True) en este caso, el personal a ingresar es chofer
    return redirect(url_for('login_client'))

def render_contacto():
    if (authenticated(session)):
        return render_template('contacto.html')
    return redirect(url_for('login'))

def render_altaChofer():
    if (authenticated(session)):
        return render_template('addChofer.html')
    return redirect(url_for('login'))

def render_login_chofer():
    return render_template("login_personal.html")

def render_altaCombi():
    return render_template('addCombi.html')  

def render_altaInsumo():
    return render_template('addInsumo.html')    
