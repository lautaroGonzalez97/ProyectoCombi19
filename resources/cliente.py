import smtplib
from models.viaje import Viaje
from models.lugar import Lugar
from models.comentario import Comentario
from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.cliente import Cliente
from models.ruta import Ruta
from models.boleto import Boleto
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import  datetime, date
from models.tarjeta import Tarjeta
from models.viaje import Viaje

def verificarSesion():
    if (not authenticated(session) or (not session["tipo"] == "Cliente")):
        abort(401)

def home():
    verificarSesion()
    prox_viaje = devolverProximo()
    proximoPost = []
    if (prox_viaje is not None):
        proximoPost.append({
            'origen': Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(prox_viaje.id_ruta).id_origen).localidad, #CUANDO NO HAY BOLETOS COMPRADOS TIRA ERROR PORQUE ES NONE --> ARREGLAR
            'destino': Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(prox_viaje.id_ruta).id_destino).localidad,
            'fecha': prox_viaje.fecha,
            'salida': prox_viaje.horaSalida,
            'llegada': prox_viaje.horaLlegada
        })
    comentarios = Comentario.all()
    comentPost=[]
    for each in comentarios:
        comentPost.append({
            'id':each.id,
            'desc': each.descripcion,
            'nomCliente': Cliente.buscarPorId(each.idCliente).nombre,
            'apeCliente': Cliente.buscarPorId(each.idCliente).apellido,
            'fecha': each.fecha
        })
    if (len(proximoPost) != 0):
        return render_template ("cliente/home.html", comentarios = comentPost, idCliente = session["id"], prox = proximoPost[0], ok= True)
    else:
        return render_template ("cliente/home.html", comentarios = comentPost, idCliente = session["id"], prox = proximoPost, ok= False)

def devolverProximo():
    boletos = Boleto.buscarBoleto() #DEVUELVE TODOS LOS BOLETOS
    viaje_prox = None
    fecha_prox = datetime.strptime((str("8000-01-01")), "%Y-%m-%d")
    for each in boletos:
        if (each.id_cliente == session["id"]) and (each.estado == 1) and (Viaje.buscarViajePorId(each.id_viaje).enabled == 1):
            fecha = datetime.strptime(str(str(Viaje.buscarViajePorId(each.id_viaje).fecha)), "%Y-%m-%d")
            if (fecha <= fecha_prox):
                viaje_prox = Viaje.buscarViajePorId(each.id_viaje)
                fecha_prox = fecha
    return viaje_prox

def render_editar_cliente (id):
    verificarSesion()
    cliente = Cliente.buscarPorId(id)
    return render_template("cliente/editClient.html", cliente = cliente)

def login():
    if (authenticated(session)):
        return redirect(url_for("home_cliente"))
    return render_template("cliente/login_client.html")

def logOut():
    if (authenticated(session)):
        del session["id"]
    return redirect(url_for("login_cliente"))

def registrar():
    return render_template("cliente/addClient.html")

def editar():
    return render_template("cliente/editClient.html")

def comprobarDatos(data):
    resultado = [True, ""]
    email = data["email"]
    emailExiste = Cliente.buscarPorEmail(email=email)
    if(emailExiste is not None):
        resultado[0] = False
        resultado[1] = "Email ya registrado en la Base de Datos"
    return resultado

def validarPassword(password):
    if (6 < len(password) <= 16):
        return True  
    else: return False  

def crear():
    cliente = request.form
    check = comprobarDatos(cliente)
    if (check[0]):
        nombre = cliente["nombre"]
        apellido = cliente["apellido"]
        email = cliente["email"]
        fechaNacimiento = cliente["fechaNacimiento"]
        password = cliente["password"]
        fechaNac = datetime.strptime(fechaNacimiento, "%Y-%m-%d")
        fecha = fechaNac + relativedelta(years=+18)
        hoy = datetime.today() 
        if (validarPassword(password)):
            if (fecha <= hoy):
                if (request.form.get('tipo') == 'isTrue'):
                    return render_template ("tarjeta/datosTarjeta.html", nom = nombre, ape = apellido, email = email, nac = fechaNacimiento, contra = password)
                new_cliente = Cliente(nombre, apellido, email, fechaNac, password)  
                new_cliente.save()
                flash ("Registro exitoso", "success")
                #probando el envio de emails
                '''message = "Usuario registrado en el sistema!"
                subject = "Registro COMBI-19"
                message = 'Subject: {}\n\n{}'.format(subject, message)
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('contacto.combi19@gmail.com', 'somoscombi19')
                server.sendmail('contacto.combi19@gmail.com', email, message)
                server.quit()'''
                return redirect(url_for("login_cliente"))
            else:
                flash ("Edad invalida", "error")
                return redirect(url_for("render_altaCliente"))
        else:
            flash ("Contraseña corta", "error")
            return redirect(url_for("render_altaCliente"))
    else:
        flash ("Email registrado en el sistema", "error")
        return redirect(url_for("render_altaCliente"))

def autenticar():
    datos = request.form
    email = datos["email"]
    password = datos["password"]
    print(email)
    print(password)
    idClient = Cliente.buscarEmailPassword(email,password)
    print(idClient)
    if (idClient is not None):
        session["id"] = idClient
        session["tipo"] = "Cliente"
        return redirect(url_for("home"))
    flash ("Email o contraseña incorrecta", "error")
    return redirect(url_for("login_cliente"))

def esGold (id):
        usuario = Cliente.buscarPorId(id)
        if ( len(usuario.tarjetas) != 0 ):
            return True
        return False

def ver_perfil():
    verificarSesion()
    perfil= Cliente.buscarPorId(session["id"])
    perfil.fechaNacimiento = datetime.strptime(str(perfil.fechaNacimiento),"%Y-%m-%d").date()
    if (esGold(perfil.id)):
        tarjetasPost=[]
        aux = perfil.tarjetas
        tarj = Tarjeta.buscarPorId(aux[0].id)
        tarjetasPost.append({
        'id':tarj.id,
        'nombre': tarj.nombre,
        'numero': tarj.numero,
        'codigo': tarj.codigo,
        'fechaVencimiento':datetime.strptime(str(tarj.fechaVencimiento),"%Y-%m-%d").date()
        })
        return render_template ("cliente/verPerfilGold.html", usuario= perfil, tarjeta= tarjetasPost[0])
    return render_template ("cliente/verPerfil.html", usuario=perfil)

def editar_cliente(id):
    verificarSesion()
    cliente = Cliente.buscarPorId(id)
    datos = request.form
    if (datos["email"]  != cliente.email):
        check = comprobarDatos(datos)
        if (check[0]):
            if (validarPassword(datos["password"])):
                fechaNac = datetime.strptime(datos["fechaNacimiento"], "%Y-%m-%d")
                fecha = fechaNac + relativedelta(years=+18)
                hoy = datetime.today() 
                if (fecha <= hoy):
                    cliente.nombre = datos["nombre"]
                    cliente.apellido = datos["apellido"]
                    cliente.email = datos["email"]
                    cliente.password = datos["password"]
                    cliente.fechaNacimiento = fechaNac
                    Cliente.actualizar(cliente)
                    flash ("Datos personales actualizados exitosamente", "success")
                    return redirect(url_for ("ver_perfil"))
                else:
                    flash ("Edad invalida", "error")
                    return redirect (url_for("render_editar_cliente", id = id))
            else:
                flash ("Contraseña corta", "error")
                return redirect (url_for("render_editar_cliente", id = id))
        else:
            flash ("Email registrado en el sistema", "error")
            return redirect (url_for("render_editar_cliente", id = id))
    else:
        if (validarPassword(datos["password"])):
            fechaNac = datetime.strptime(datos["fechaNacimiento"], "%Y-%m-%d")
            fecha = fechaNac + relativedelta(years=+18)
            hoy = datetime.today() 
            if (fecha <= hoy):
                cliente.nombre = datos["nombre"]
                cliente.apellido = datos["apellido"]
                cliente.email = datos["email"]
                cliente.password = datos["password"]
                cliente.fechaNacimiento = fechaNac
                Cliente.actualizar(cliente)
                flash ("Datos personales actualizados exitosamente", "success")
                return redirect(url_for ("ver_perfil"))
            else:
                flash ("Edad invalida", "error")
                return redirect (url_for("render_editar_cliente", id = id))
        else:
            flash ("Contraseña corta", "error")
            return redirect (url_for("render_editar_cliente", id = id))

def buscarViaje(origen, destino, fecha):
    ruta = Ruta.buscarRutaPorOrigenYDestino(origen, destino)
    if (ruta is not None):
        viajes = []
        for viaje in ruta.viajes:
            if (viaje.fecha == fecha) and (viaje.enabled == 1):
                viajes.append({
                    'id': viaje.id,
                    'origen': origen,
                    'destino': destino,
                    'fecha': viaje.fecha,
                    'salida': viaje.horaSalida,
                    'llegada': viaje.horaLlegada,
                    'asientos': viaje.asientos_disponibles,
                    'precio': viaje.precio
                })
        return viajes
    else:
        return None

def busqueda ():
    verificarSesion()
    datos = request.form
    origen = datos['origen']
    destino = datos['destino']
    fecha = datos['fecha']
    fecha_viaje = datetime.strptime(fecha, "%Y-%m-%d").date()
    hoy = date.today() 
    if (origen != destino):
        if (fecha_viaje >= hoy):
            viajes = buscarViaje(origen, destino, fecha_viaje)
            if (viajes is not None):
                if (len(viajes) != 0):
                    return render_template('cliente/resultadoBusqueda.html', viajes = viajes)
                else:
                    flash("¡Ups! No hay viaje para la fecha buscada", "warning")
                    return redirect(url_for('home_cliente'))
            else:
                flash("¡Error! Por el momento no  hay viajes para ese origen y destino", "error")
                return redirect(url_for('home_cliente')) 
        else:
            flash("¡Error! Fecha de viaje invalida", "error")
            return redirect(url_for('home_cliente'))
    else:
        flash("¡Error! Ingrese un origen y destino distintos", "error")
        return redirect(url_for('home_cliente'))

def ver_mis_viajes():
    verificarSesion()
    mis_viajes = Boleto.buscarBoleto()
    boletoPost = []
    estados=["PENDIENTE","EN CURSO","FINALIZADO","CANCELADO","RECHAZADO", "AUSENTE" ,"VIAJE ELIMINADO", "CANCELADO POR CHOFER"]
    for each in mis_viajes:
        if (each.id_cliente == session["id"]):
            boletoPost.append({
                'id': each.id,
                "origen": Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(Viaje.buscarViajePorId(each.id_viaje).id_ruta).id_origen).localidad,
                "destino": Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(Viaje.buscarViajePorId(each.id_viaje).id_ruta).id_destino).localidad,
                "fecha": Viaje.buscarViajePorId(each.id_viaje).fecha,
                "salida":Viaje.buscarViajePorId(each.id_viaje).horaSalida,
                'llegada': Viaje.buscarViajePorId(each.id_viaje).horaLlegada,
                'asientos': Viaje.buscarViajePorId(each.id_viaje).asientos_disponibles,
                'precio': Viaje.buscarViajePorId(each.id_viaje).precio,
                'estado': estados[each.estado -1],
                'asientos': each.cantidad_boletos
            })
    if (len(boletoPost) == 0):
        flash ("No haz realizado compras hasta el momento", "warning")
    return render_template("viaje/verMisViajes.html", viajes = boletoPost)

