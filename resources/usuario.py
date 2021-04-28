from flask import render_template, session, redirect, url_for, flash, request
from helpers.auth import authenticated

def render_login():
    return render_template("login.html")

def render_register():
    return render_template("register.html")

def render_home():
    return render_template('home.html')

def contacto():
    return render_template('contacto.html')
