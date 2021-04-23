from flask import Flask, render_template, redirect, url_for, session, request, flash
from resources import usuario
from flask_mysqldb import MySQL

app = Flask (__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "combi_19"
mysql = MySQL(app)

app.secret_key = 'esto-es-una-clave-muy-secreta'

#Rutas Usuarios
app.add_url_rule("/iniciar_sesion","login", usuario.login)
#app.add_url_rule("/autenticacion", "autenticar_login", usuario.autenticar, methods=["POST"])
#app.add_url_rule("/cerrar_sesion", "logout", usuario.logout)
#app.add_url_rule("/registrar", "registrar", usuario.registrar, methods=["POST"])


#Esto es para cuando ingresan a la pagina, si su id no esta en Session los tira al template login, sino entran a la pagina (#)
'''@app.route('/')
def home():
    if (not 'id' in session):
        return redirect(url_for("login"))
    return redirect(url_for('#')) #redirije a home'''

@app.route("/")
def home ():
    return render_template("login.html")

@app.route("/registrar" , methods=["POST"])
def registrar():
    if (request.method == "POST"):
        datos = request.form
        email = datos["email"]
        password = datos["password"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (email, password) VALUES (%s, %s)", (email, password))
        mysql.connection.commit()
        return redirect(url_for("login"))

@app.route("/autenticar" , methods=["POST"])
def autenticar ():
    datos = request.form 
    email = datos["email"]
    password = datos["password"]
    cur = mysql.connection.cursor()
    idUser = cur.execute("SELECT id FROM usuario WHERE (email = %s) and (password = %s)", (email, password))
    if (idUser != 0):
        session["id"] = idUser
        return render_template("home.html")
    else:
        print("entro mal los datos")
        flash ("Correo o clave incorrecta") #no muestra mensaje flash, porque?
        return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(port= 8080, debug=True)