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
#app.add_url_rule("/iniciar_sesion","login", usuario.render_login)
# app.add_url_rule("/registrar_usuario","register", usuario.render_register)
app.add_url_rule("/home","home", usuario.render_home) #Hay que mandarle un identificador para tipo y ese identificador despues es evaluado en el html para ver que home muestra
app.add_url_rule("/contacto","contacto", usuario.render_contacto)
#Rutas de para renderizar templates
app.add_url_rule("/iniciar_sesion","login_client", usuario.render_login_client)
app.add_url_rule("/registrar_usuario","add_client", usuario.render_register_client)
app.add_url_rule("/contacto","contact", usuario.render_contacto)
app.add_url_rule("/alta_chofer","add_chofer", usuario.render_altaChofer)
app.add_url_rule("/iniciar_sesion_personalEmpresa","login_personal_empresa", usuario.render_login_personal_empresa)

#Esto es para cuando ingresan a la pagina, si su id no esta en Session los tira al template login, sino entran a la pagina (#)
@app.route('/')
def index():
    if (not 'id' in session):
        return redirect(url_for("login_client"))
    return redirect(url_for('home'))


@app.route('/contactos')
def contactos():
    return redirect(url_for('contacto'))

@app.route('/homePersonalEmpresa')
def homePersonalEmpresa():
    return render_template('homePersonalEmpresa.html')

#--------------- ABM CLIENTE ---------------
@app.route("/altaUsuario" , methods=["POST"])
def altaUsuario():
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
        #Falta validar el tema de que la contrasenia tenga 6 caracteres y que el email no exista en la bd
        if (fecha <= hoy):
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO cliente (nombre, apellido, email, fechaNacimiento, password) VALUES (%s, %s, %s, %s, %s)", 
                (nombre, apellido, email, fechaNac, password))
            mysql.connection.commit()
            if request.form.get('tipo') == 'isTrue':
                # recuperar id
                idClient = cur.execute ("SELECT id FROM cliente WHERE email = %s", (email,))
                return render_template("datosTarjeta.html", id = idClient)
            flash("Registro exitoso", "success")
            return redirect(url_for("login_client"))
        else:
            flash("Edad invalida para registrarse", "error")
            return redirect(url_for("add_client"))

@app.route("/bajaCliente/<id>")
def bajaCliente(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cliente WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for("login_client")) #refresca la pagina y no esta mas el chofer que elimino

@app.route("/editarCliente/<id>")
def getCliente(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cliente WHERE id = %s", (id,))
    data = cur.fetchall()
    if (authenticated(session)): #ARREGLAR ESTO QUE QUEDA CHANCHO, TENDRIA QUE ESTAR EN USUARIO.RENDER_EDITARCHOFER
        return render_template('editClient.html', cliente = data[0]) 
    return redirect(url_for('login_client'))

@app.route("/actualizarCliente/<id>", methods=["POST"])
def actualizarCliente(id):
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
            cur.execute("UPDATE cliente SET nombre = %s, apellido = %s, email = %s, fechaNacimiento = %s, password = %sWHERE id = %s ", 
                (nombre, apellido, email, fechaNac, password,id))
            mysql.connection.commit()
            return redirect(url_for("home")) #vuelvo a la lista de usuarios (falta hacer)
        return redirect(url_for("home"))

#------------------ Alta de Tarjeta para Cliente -------------------
@app.route ("/agregarTarjeta/<id>", methods=["POST"])
def agregarTarjeta(id):
    if (request.method == "POST"):
        datos = request.form
        nombre = datos["nombre"]
        numero = datos["numero"]
        fechaVencimiento = datos["fechaVencimiento"]
        codSeguridad = datos["codSeguridad"]
        # if (numero.length() == 16):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tarjeta_credito (nombre,numero,codSeguridad,id_cliente,fechaVencimiento) VALUES (%s,%s,%s,%s,%s)", (nombre,numero,codSeguridad,id,fechaVencimiento))
        cur.connection.commit()
        flash("Registro exitoso", "success")
        return redirect(url_for("login_client"))
        # else:
        #     flash("Numero de tarjeta incorrecto", "error")
        #     return redirect(url_for("add_client"))

#------------------ login cliente ------------------
@app.route("/autenticarCliente" , methods=["POST"])
def autenticarCliente():
    if (request.method == "POST"):
        datos = request.form 
        email = datos["email"]
        password = datos["password"]
        cur = mysql.connection.cursor()
        idUser = cur.execute("SELECT id FROM cliente WHERE (email = %s) and (password = %s)", (email, password))
        if (idUser != 0):
            session["id"] = idUser
            return redirect(url_for("home"))
        else:
            flash("Correo o clave incorrecta", "error")
            return redirect(url_for("login_client"))

#--------------- ABM PERSONAL DE LA EMPRESA --------------- CHOFER = PERSONAL_EMPRESA HAY QUE CAMBIAR LOS NOMBRES DE LOS METODOS Y SUS LLAMADOS
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
        cur.execute("INSERT INTO personal_empresa (nombre, apellido, email, documento, password) VALUES (%s, %s, %s, %s, %s)", 
            (nombre, apellido, email, doc_numero, password))
        mysql.connection.commit()
        flash("Alta de chofer exitosa", "success")
        return redirect(url_for("home")) #vuelvo al template que me invoco

@app.route("/bajaChofer/<id>")
def bajaChofer(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM personal_empresa WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for("login_client")) #refresca la pagina y no esta mas el chofer que elimino

@app.route("/autenticar" , methods=["POST"])
def autenticar ():
    datos = request.form 
    email = datos["email"]
    password = datos["password"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM personal_empresa WHERE id = %s", (id,))
    data = cur.fetchall()
    if (authenticated(session)): #ARREGLAR ESTO QUE QUEDA CHANCHO, TENDRIA QUE ESTAR EN USUARIO.RENDER_EDITARCHOFER
        return render_template('editChofer.html', chofer = data[0])
    return redirect(url_for('login_client'))

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
        cur.execute("UPDATE personal_empresa SET nombre = %s, apellido = %s, email = %s, documento = %s, password = %sWHERE id = %s ", 
            (nombre, apellido, email, doc_numero, password,id))
        mysql.connection.commit()
        flash("Actualizacion exitosa")
        return redirect(url_for("home")) #vuelvo a la lista de choferes (falta hacer) 

#------------------ login chofer ------------------
@app.route("/autenticarChofer" , methods=["POST"])
def autenticarChofer ():
    if (request.method == "POST"):
        datos = request.form 
        email = datos["email"]
        password = datos["password"]
        cur = mysql.connection.cursor()
        idUser = cur.execute("SELECT id FROM personal_empresa WHERE (email = %s) and (password = %s)", (email, password))
        if (idUser != 0):
            session["id"] = idUser
            if datos['tipo'] == 'isTrue':
                return redirect(url_for("home", tipo = administrado ))
            else:   
                return redirect(url_for("homePersonalEmpresa", tipo= chofer))
        else:
            flash("Correo o clave incorrecta", "error")
            return redirect(url_for("login_personal_empresa"))

@app.route ("/logOut")
def logOut():
    if (authenticated(session)):
        del session['id'] 
    return redirect (url_for('login_client'))

if __name__ == '__main__':
    app.run(port= 8080, debug=True)