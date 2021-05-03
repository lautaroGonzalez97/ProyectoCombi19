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
app.add_url_rule("/iniciar_sesion","login_client", usuario.render_login_client)
app.add_url_rule("/registrar_usuario","add_user", usuario.render_register)
app.add_url_rule("/home","home", usuario.render_home)
app.add_url_rule("/contacto","contact", usuario.render_contacto)
app.add_url_rule("/alta_chofer","add_chofer", usuario.render_altaChofer)
app.add_url_rule("/iniciar_sesion_personalEmpresa","login_chofer", usuario.render_login_chofer)
app.add_url_rule("/alta_combi","add_combi", usuario.render_altaCombi)


#Esto es para cuando ingresan a la pagina, si su id no esta en Session los tira al template login, sino entran a la pagina (#)
@app.route('/')
def index():
    if (not 'id' in session):
        return redirect(url_for("login_client"))
    return redirect(url_for('home'))

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
        if (fecha <= hoy):
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO cliente (nombre, apellido, email, fechaNacimiento, password) VALUES (%s, %s, %s, %s, %s)", 
                (nombre, apellido, email, fechaNac, password))
            mysql.connection.commit()
            flash("Registro exitoso", "success")
            return redirect(url_for("login_client"))
        else:
            flash("Edad invalida para registrarse", "error")
            return redirect(url_for("add_user"))

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

#--------------- ABM CHOFER --------------- CHOFER = PERSONAL_EMPRESA HAY QUE CAMBIAR LOS NOMBRES DE LOS METODOS Y SUS LLAMADOS
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
    return redirect(url_for("listarChoferes")) #refresca la pagina y no esta mas el chofer que elimino

@app.route("/editarChofer/<id>")        
def getChofer(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM personal_empresa WHERE id = %s", (id,))
    data = cur.fetchall()
    if (authenticated(session)): #ARREGLAR ESTO QUE QUEDA CHANCHO, TENDRIA QUE ESTAR EN USUARIO.RENDER_EDITARCHOFER
        return render_template('editChofer.html', chofer = data[0])
    return redirect(url_for('listarChoferes'))

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
        return redirect(url_for("listarChoferes")) #vuelvo a la lista de choferes (falta hacer) 






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
            return redirect(url_for("home"))
        else:
            flash("Correo o clave incorrecta", "error")
            return redirect(url_for("login_chofer"))




#--------------- ABM Combi ----------------
@app.route("/altaCombi" , methods=["POST"])
def altaCombi():
    if (request.method == "POST"):
        datos = request.form
        patente = datos["Patente"]
        año = datos["Año"]
        modelo = datos["Modelo"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO combis (patente, año, modelo) VALUES (%s, %s, %s)", 
            (patente, año, modelo))
        mysql.connection.commit()
        flash("Alta de combi exitosa", "success")
        return redirect(url_for("home")) #vuelvo al template que me invoco

@app.route("/editarCombi/<id>")      
def getCombi(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM combis WHERE id = %s", (id,))
    data = cur.fetchall()
    if (authenticated(session)): #ARREGLAR ESTO QUE QUEDA CHANCHO, TENDRIA QUE ESTAR EN USUARIO.RENDER_EDITARCHOFER
        return render_template('editCombi.html', combi = data[0])
    return redirect(url_for('listarCombis'))    

@app.route("/bajaCombi/<id>")    
def bajaCombi(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM combis WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for("listarCombis")) #refresca la pagina y no esta mas el chofer que elimino     


@app.route("/actualizarCombi/<id>", methods=["POST"])          
def actualizarCombi(id):
    if (request.method == "POST"):
        datos = request.form
        patente = datos["patente"]
        año = datos["año"]
        modelo = datos["modelo"]
        cur = mysql.connection.cursor()
        cur.execute("UPDATE combis SET patente = %s, año = %s, modelo = %s", (patente, año, modelo))
        mysql.connection.commit()
        flash("Actualizacion exitosa")
        return redirect(url_for("listarCombis")) #vuelvo a la lista de choferes (falta hacer)     


#----------- LISTAR ------------------

#---combi ---
@app.route("/listarCombis")
def listarCombis():
    cur=  mysql.connection.cursor()
    cur.execute(" SELECT * FROM combis")
    data= cur.fetchall()
    return render_template('listaCombis.html', listaCombi = data)    

#---chofer---
@app.route("/listarChoferes")
def listarChofer():
    cur=  mysql.connection.cursor()
    cur.execute(" SELECT * FROM personal_empresa")
    data= cur.fetchall()
    return render_template('listaChoferes.html', empleados = data)





@app.route ("/logOut")
def logOut():
    if (authenticated(session)):
        del session['id'] 
    return redirect (url_for('login_client'))

if __name__ == '__main__':
    app.run(port= 8080, debug=True)