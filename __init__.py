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
app.add_url_rule("/iniciar_sesion_personalEmpresa","login_chofer", usuario.render_login_chofer)
app.add_url_rule("/alta_combi","add_combi", usuario.render_altaCombi)
app.add_url_rule("/alta_insumo","add_insumo", usuario.render_altaInsumo)


#Esto es para cuando ingresan a la pagina, si su id no esta en Session los tira al template login, sino entran a la pagina (#)
@app.route('/')
def index():
    if (not 'id' in session):
        return redirect(url_for("login_client"))
    return redirect(url_for('home'))


@app.route('/contactos')
def contactos():
    return redirect(url_for('contacto'))

@app.route('/homeChofer')
def homeChofer():
    return render_template('homeChofer.html')

@app.route('/homeAdmin')
def homeAdmin():
    return render_template('homeAdmin.html') 

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
        if (validarPassword(password) and (fecha <= hoy)):
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO cliente (nombre, apellido, email, fechaNacimiento, password) VALUES (%s, %s, %s, %s, %s)", 
                (nombre, apellido, email, fechaNac, password))
            mysql.connection.commit()
            if request.form.get('tipo') == 'isTrue':
                # recuperar id
                idClient = cur.execute ("SELECT id FROM cliente WHERE email = %s", (email,))
                return render_template("datosTarjeta.html", idC = idClient)
                # Deberia ejecutarse y luego agregar el usuario. Si carga mal la tarjeta no tendria que cargarse el usuario 
            flash("Registro exitoso", "success")
            return redirect(url_for("login_client"))
        else:
            if (fecha > hoy):
                flash("Edad invalida para registrarse", "error")
                return redirect(url_for("add_user"))
            else:
                flash("La contraseña debe superar los 6 caracteres", "error")
                return redirect(url_for("add_user"))


#------valida que contraseña sea mayor que 6 e igual o menor que 16 --------
def validarPassword(password):
    if 6 < len(password) <= 16:
        return True  
    else: return False        




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
@app.route ("/agregarTarjeta/<idC>", methods=["GET","POST"])
def agregarTarjeta(idC):
    if (request.method == "POST"):
        datos = request.form
        nombre = datos["nombre"]
        numero = datos["numero"]
        fechaVencimiento = datos["fechaVencimiento"]
        codSeguridad = datos["codSeguridad"]
        if (len(numero) == 16):
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tarjeta_credito (nombre,numero,codSeguridad,id_cliente,fechaVencimiento) VALUES (%s,%s,%s,%s,%s)", (nombre,numero,codSeguridad,idC,fechaVencimiento))
            cur.connection.commit()
            flash("Registro exitoso", "success")
            return redirect(url_for("login_client"))
        else:
            flash("Numero de tarjeta incorrecto", "error")
            return redirect(url_for("add_client"))

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
        telefono = datos["telefono"]
        password = datos["password"]
        tipo = 2
        if (len(password) > 6):
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO personal_empresa (nombre, apellido, email, telefono, password, tipo) VALUES (%s, %s, %s, %s, %s, %s)", 
                (nombre, apellido, email, telefono, password, tipo))
            mysql.connection.commit()
            flash("Alta de chofer exitosa", "success")
            return redirect(url_for("home")) #vuelvo al template que me invoco
        else: 
            flash ("La Contraseña debe superar los 6 caracteres", "error")    # NO ESTA INFORMANDO EL ERROR DE LOS CARACTERES. PERO BIEN, NO HACE EL ALTA
            return redirect(url_for("add_chofer"))    
       


@app.route("/bajaChofer/<id>")    
def bajaChofer(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM personal_empresa WHERE id = {0}".format(id))
    mysql.connection.commit()
    flash ("Se elimino el chofer","success")
    return redirect(url_for("listarChoferes")) #refresca la pagina y no esta mas el chofer que elimino

@app.route("/editarChofer/<id>")        
def getChofer(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM personal_empresa WHERE id = %s", (id,))
    data = cur.fetchall()
    if (authenticated(session)): #ARREGLAR ESTO QUE QUEDA CHANCHO, TENDRIA QUE ESTAR EN USUARIO.RENDER_EDITARCHOFER
        flash ("Chofer editado exitosamente","success")
        return render_template('editChofer.html', chofer = data[0])
    flash ("Chofer editado exitosamente","success")
    return redirect(url_for('listarChoferes'))

@app.route("/actualizarChofer/<id>", methods=["POST"])          
def actualizarChofer(id):
    if (request.method == "POST"):
        datos = request.form
        nombre = datos["nombre"]
        apellido = datos["apellido"]
        email = datos["email"]
        telefono = datos["telefono"]
        password = datos["password"]
        cur = mysql.connection.cursor()
        cur.execute("UPDATE personal_empresa SET nombre = %s, apellido = %s, email = %s, telefono = %s, password = %sWHERE id = %s ", 
            (nombre, apellido, email, telefono, password,id))
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
        tipo = cur.execute("SELECT tipo FROM personal_empresa WHERE (email = %s) and (password = %s)", (email, password))
        if (idUser != 0):
            session["id"] = idUser
            session["tipo"] = tipo
            print (type(tipo))
            print (tipo)
            if tipo == 1:
                return redirect(url_for("homeAdmin"))
            else:   
                return redirect(url_for("homeChofer"))
        else:
            flash("Correo o clave incorrecta", "error")
            return redirect(url_for("login_personal_empresa"))




#--------------- ABM Combi ----------------
@app.route("/altaCombi" , methods=["POST"])
def altaCombi():
    if (request.method == "POST"):
        datos = request.form
        modelo = datos["modelo"]
        patente = datos["patente"]
        asientos_docstring = datos["asientos"]
        tipo = datos["tipo"]
        id_chofer_docstring = datos ["id_chofer"]    #----ESTA MAL, NO EVALUO QUE EL ID_CHOFER EXISTA
        asientos_num = int(asientos_docstring)
        id_chofer = int(id_chofer_docstring)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO combi (modelo, patente, asiento, tipo, id_chofer) VALUES (%s, %s, %s, %s, %s)", 
            (modelo, patente, asientos_num, tipo, id_chofer))
        mysql.connection.commit()
        flash("Alta de combi exitosa", "success")
        return redirect(url_for("home")) #vuelvo al template que me invoco

@app.route("/editarCombi/<id>")      
def getCombi(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM combi WHERE id = %s", (id,))
    data = cur.fetchall()
    if (authenticated(session)): #ARREGLAR ESTO QUE QUEDA CHANCHO, TENDRIA QUE ESTAR EN USUARIO.RENDER_EDITARCHOFER
        return render_template('editCombi.html', combi = data[0])
    return redirect(url_for('listarCombis'))    

@app.route("/bajaCombi/<id>")    
def bajaCombi(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM combi WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for("listarCombis")) #refresca la pagina y no esta mas el chofer que elimino     


@app.route("/actualizarCombi/<id>", methods=["POST"])          
def actualizarCombi(id):
    if (request.method == "POST"):
        datos = request.form
        patente = datos["patente"]
        modelo = datos["modelo"]
        asientos_docstring = datos["asientos"]
        tipo = datos["tipo"]
        id_chofer_docstring = datos ["id_chofer"]    #----ESTA MAL, NO EVALUO QUE EL ID_CHOFER EXISTA
        asientos_num = int(asientos_doctring)
        id_chofer = int(id_chofer_docstring)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE combis SET modelo = %s, patente = %s, asientos = %s, tipo = %s, id_chofer = %s", (modelo, patente, asientos, tipo, id_chofer))
        mysql.connection.commit()
        flash("Actualizacion exitosa")
        return redirect(url_for("listarCombis")) #vuelvo a la lista de combis     


#---------- ABM INSUMO -----------
@app.route("/altaInsumo" , methods=["POST"])
def altaInsumo():
    if (request.method == "POST"):
        datos = request.form
        nombre = datos["nombre"]
        tipo = datos["tipo"]
        precio = datos["precio"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO insumo (nombre, tipo, precio) VALUES (%s, %s, %s)", 
            (nombre, tipo, precio))
        mysql.connection.commit()
        flash("Alta de insumo exitosa", "success")
        return redirect(url_for("home")) #vuelvo al template que me invoco

@app.route("/editarInsumo/<id>")      
def getInsumo(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM insumo WHERE id = %s", (id,))
    data = cur.fetchall()
    if (authenticated(session)): #ARREGLAR ESTO QUE QUEDA CHANCHO, TENDRIA QUE ESTAR EN USUARIO.RENDER_EDITARCHOFER
        return render_template('editInsumo.html', insumo = data[0])
    return redirect(url_for('listarInsumos'))    

@app.route("/bajaInsumo/<id>")    
def bajaInsumo(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM insumo WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for("listarInsumos")) #refresca la pagina y no esta mas el chofer que elimino     


@app.route("/actualizarInsumo/<id>", methods=["POST"])          
def actualizarInsumo(id):
    if (request.method == "POST"):
        datos = request.form
        nombre = datos["nombre"]
        tipo = datos["tipo"]
        precio = datos["precio"]
        cur = mysql.connection.cursor()
        cur.execute("UPDATE insumo SET nombre = %s, tipo = %s, precio = %s",( nombre, tipo, precio))
        mysql.connection.commit()
        flash("Actualizacion exitosa")
        return redirect(url_for("listarInsumos")) #vuelvo a la lista de choferes (falta hacer)  




#----------- LISTAR ------------------

#---combi ---
@app.route("/listarCombis")
def listarCombis():
    cur=  mysql.connection.cursor()
    cur.execute(" SELECT * FROM combi")
    data= cur.fetchall()
    return render_template('listaCombis.html', listaCombi = data)    

#---chofer---
@app.route("/listarChoferes")
def listarChoferes():
    cur=  mysql.connection.cursor()
    cur.execute(" SELECT * FROM personal_empresa")
    data= cur.fetchall()
    return render_template('listaChoferes.html', empleados = data)

#---Insunmo ---
@app.route("/listarInsumos")
def listarInsumos():
    cur=  mysql.connection.cursor()
    cur.execute(" SELECT * FROM insumo")
    data= cur.fetchall()
    return render_template('listaInsumos.html', listaInsumos = data)







@app.route ("/logOut")
def logOut():
    if (authenticated(session)):
        del session['id'] 
    return redirect (url_for('login_client'))

if __name__ == '__main__':
    app.run(port= 8080, debug=True)




