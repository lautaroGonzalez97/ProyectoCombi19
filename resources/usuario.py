from flask import render_template, session, redirect, url_for, flash, request
from helpers.auth import authenticated

def render_login():
    return render_template("login.html")

def render_register():
    return render_template('register.html')

def render_home():
    if (authenticated(session)):
        return render_template('home.html')
    return redirect(url_for('login'))

def render_contacto():
    if (authenticated(session)):
        return render_template('contacto.html')
    return redirect(url_for('login'))

def render_altaChofer():
    if (authenticated(session)):
        return render_template('addChofer.html')
    return redirect(url_for('login'))

'''def render_editarChofer():
    if (authenticated(session)):
        return render_template('editChofer.html')
    return redirect(url_for('login'))'''