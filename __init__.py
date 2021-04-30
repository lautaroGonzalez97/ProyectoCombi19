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

#confuguracion base de datos
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "combi_19"
mysql = MySQL(app)

#configuracion de session
app.secret_key = 'esto-es-una-clave-muy-secreta'

#Rutas de para renderizar templates
app.add_url_rule("/iniciar_sesion","login", usuario.render_login)
app.add_url_rule("/registrar_usuario","register", usuario.render_register)
app.add_url_rule("/home","home", usuario.render_home)
app.add_url_rule("/contacto","contacto", usuario.render_contacto)
app.add_url_rule("/alta_chofer","alta_chofer", usuario.render_altaChofer)
#app.add_url_rule("/editar_chofer","editar_chofer", usuario.render_editarChofer)

#Esto es para cuando ingresan a la pagina, si su id no esta en Session los tira al template login, sino entran a la pagina (#)
@app.route('/')
def index():
    if (not 'id' in session):
        return redirect(url_for("login"))
    return redirect(url_for('home'))

#Metodo que llama el template register para registrar a un usuario  
@app.route("/registrar" , methods=["POST"])
def registrar():
    if (request.method == "POST"):
        datos = request.form
        nombre = datos["nombre"]
        apellido = datos["apellido"]
        email = datos["email"]
        nacimiento = datos["fechaNacimiento"]
        password = datos["password"]
        fechaNac = datetime.strptime(nacimiento, "%Y-%m-%d")
        fecha = fechaNac + relativedelta(years=+18)
        hoy = datetime.today()
        if (fecha <= hoy):
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO usuario (nombre, apellido, email, fechaNacimiento, password) VALUES (%s, %s, %s, %s, %s)", 
                (nombre, apellido, email, fechaNac, password))
            mysql.connection.commit()
            flash("Registro exitoso", "success")
            return redirect(url_for("login"))
        else:
            flash("Edad invalida para registrarse", "error")
            return redirect(url_for("register"))
    
#Metodo que llama el template login para ver si el email y pass son correctos
@app.route("/autenticar" , methods=["POST"])
def autenticar ():
    if (request.method == "POST"):
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

#--------------- ABM CHOFER ---------------
@app.route("/altaChofer" , methods=["POST"])
def altaChofer():
    if (request.method == "POST"):
        datos = request.form
        nombre = datos["nombre"]
        apellido = datos["apellido"]
        email = datos["email"]
        doc_string = datos["documento"]
        password = datos["password"]
        cur = mysql.connection.cursor()
        doc_numero = int(doc_string)
        cur.execute("INSERT INTO chofer (nombre, apellido, email, documento, password) VALUES (%s, %s, %s, %s, %s)", 
            (nombre, apellido, email, doc_numero, password))
        mysql.connection.commit()
        flash("Alta de chofer exitosa", "success")
        return redirect(url_for("home")) #vuelvo al template que me invoco

@app.route("/bajaChofer/<id>")
def bajaChofer(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM chofer WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for("login")) #refresca la pagina y no esta mas el chofer que elimino

@app.route("/editarChofer/<id>")
def getChofer(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM chofer WHERE id = %s", (id))
    data = cur.fetchall()
    if (authenticated(session)): #ARREGLAR ESTO QUE QUEDA CHANCHO, TENDRIA QUE ESTAR EN USUARIO.RENDER_EDITARCHOFER
        return render_template('editChofer.html', chofer = data[0])
    return redirect(url_for('login'))

@app.route("/actualizarChofer/<id>", methods=["POST"])
def actualizarChofer(id):
    if (request.method == "POST"):
        datos = request.form
        nombre = datos["nombre"]
        apellido = datos["apellido"]
        email = datos["email"]
        doc_string = datos["documento"]
        password = datos["password"]
        doc_numero = int(doc_string)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE chofer SET nombre = %s, apellido = %s, email = %s, documento = %s, password = %sWHERE id = %s ", 
            (nombre, apellido, email, doc_numero, password,id))
        mysql.connection.commit()
        flash("Actualizacion exitosa")
        return redirect(url_for("home")) #vuelvo a la lista de choferes (falta hacer) 

@app.route ("/logOut")
def logOut():
    if (authenticated(session)):
        del session['id'] 
    return redirect (url_for('login'))

if __name__ == '__main__':
    app.run(port= 8080, debug=True)