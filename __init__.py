from flask import Flask, render_template, redirect, url_for, session, request, flash
#para trabajar fechas
from datetime import datetime
from dateutil.relativedelta import relativedelta #pip install python-dateutil
#base de datos
from flask_mysqldb import MySQL
#funcionalidades
from resources import usuario
from helpers.auth import authenticated 


app = Flask (__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "combi_19"
mysql = MySQL(app)

app.secret_key = 'esto-es-una-clave-muy-secreta'

#Rutas Usuarios
app.add_url_rule("/iniciar_sesion","login", usuario.render_login)
app.add_url_rule("/registrar_usuario","register", usuario.render_register)
app.add_url_rule("/home","home", usuario.render_home)
app.add_url_rule("/contacto","contacto", usuario.contacto)

#Esto es para cuando ingresan a la pagina, si su id no esta en Session los tira al template login, sino entran a la pagina (#)
@app.route('/')
def index():
    if (not 'id' in session):
        return redirect(url_for("login"))
    return redirect(url_for('home'))

@app.route("/registrar" , methods=["POST"])
def registrar():
    datos = request.form
    nombre = datos["nombre"]
    apellido = datos["apellido"]
    username = ["username"]
    email = datos["email"]
    nacimiento = datos["fechaNacimiento"]
    password = datos["password"]
    fechaNac = datetime.strptime(nacimiento, "%Y-%m-%d")
    fecha = fechaNac + relativedelta(years=+18)
    hoy = datetime.today()
    print (type(fecha))
    if (fecha <= hoy):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (nombre, apellido, username, email, fechaNacimiento, password) VALUES (%s, %s, %s, %s, %s, %s)", (nombre, apellido, username, email, fechaNac, password))
        mysql.connection.commit()
        flash("Registrado correctamente", "success")
        return redirect(url_for("login"))
    else:
        flash("Edad invalida para registrarse", "error")
        return redirect(url_for("register"))
    

@app.route("/autenticar" , methods=["POST"])
def autenticar ():
    datos = request.form 
    email = datos["email"]
    password = datos["password"]
    cur = mysql.connection.cursor()
    idUser = cur.execute("SELECT id FROM usuario WHERE (email = %s) and (password = %s)", (email, password))
    if (idUser != 0):
        session["id"] = idUser
        return redirect(url_for("home"))
    else:
        flash("Correo o clave incorrecta", "error")
        return redirect(url_for("login"))

@app.route ("/logOut")
def logOut():
    if (authenticated(session)):
        del session['id'] 
    return redirect (url_for('login'))

if __name__ == '__main__':
    app.run(port= 8080, debug=True)