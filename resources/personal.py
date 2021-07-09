from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.personal import Personal
from models.comentario import Comentario
from models.cliente import Cliente
from models.ruta import Ruta
from models.viaje import Viaje
from models.lugar import Lugar
from models.boleto import Boleto

def verificarSesionChofer():
    if (not (authenticated(session)) or (not (session["tipo"] == "Chofer"))):
        abort(401)

def verificarSesionAdmin():
    if (not (authenticated(session)) or (not (session["tipo"] == "Admin"))):
        abort(401)

def verificarSesionPersonal():
    if (not (authenticated(session))):
        abort(401)
    if not (not (session["tipo"] == "Admin") and (session["tipo"] == "Chofer") or ((session["tipo"] == "Admin") and (not (session["tipo"] == "Chofer")))):
        abort(401)

def home_chofer():
    verificarSesionChofer()
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
    if len(comentarios) == 0 :
        flash ("No hay comentarios", "warning")
    return render_template ("personal/home.html", comentarios = comentPost, tipo = session["tipo"])
    
def home_admin():
    verificarSesionAdmin()
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
    if len(comentarios) == 0 :
        flash ("No hay comentarios", "warning")
    return render_template ("personal/home.html", comentarios = comentPost, tipo = session["tipo"])
    
def listado_chofer():
    verificarSesionAdmin()
    personal = Personal.all()
    choferes = list (filter(lambda x: x.tipo == 2, personal))
    if len(choferes) == 0:
        flash ("No hay choferes cargados", "warning")
    return render_template("personal/listaChoferes.html", choferes = choferes)
    
def render_alta_chofer():
    verificarSesionAdmin()
    return render_template("personal/addChofer.html")

def render_editar_chofer(id):
    verificarSesionPersonal()
    chofer = Personal.buscarChoferPorId(id)
    if (session["tipo"] == "Admin"):
        return render_template("personal/editChofer.html", chofer = chofer)
    else:
        return render_template("personal/editPerfilPersonal.html", chofer = chofer)

def render_datosCovid(idP, idV):
    return render_template("personal/cargaDatosCOVID.html", idP = idP, idV = idV)

def login():
    if (authenticated(session)):
        return redirect(url_for("home_personal"))
    return render_template("personal/login_personal.html")

def logOut():
    if (authenticated(session)):
        del session["id"]
    return redirect(url_for("login_personal"))

def listaChoferes():
    personal = Personal.all()
    choferes = list (filter(lambda x: x.tipo == 2, personal))
    return choferes

def ver_perfil_personal():
    verificarSesionChofer()
    perfil= Personal.buscarChoferPorId(session["id"])
    return render_template ("personal/verPerfilPersonal.html", usuario=perfil)

def autenticar():
    datos = request.form
    email = datos["email"]
    password = datos["password"]
    info = Personal.buscarEmailPassword(email,password)
    if (info[0] is None):
        flash ("Email o contraseña incorrecta", "error")
        return redirect(url_for("login_personal"))
    else:
        if (info[1] == 2):
            session["id"] = info[0] 
            session["tipo"] = "Chofer"
            return redirect(url_for("home_chofer")) 
        else:
            session["id"] = info[0]  
            session["tipo"] = "Admin"
            return redirect(url_for("home_admin"))

def validarPassword(password):
    """
    Valida que la contraseña sea mayor que 6, y menor o igual a 16 
    """
    if (6 < len(password) <= 16):
        return True  
    else: return False  

def alta_chofer():
    chofer = request.form
    nombre = chofer["nombre"]
    apellido = chofer["apellido"]
    email = chofer["email"]
    telefono = chofer["telefono"]
    password = chofer["password"]
    if (validarPassword(password)) and (validarEmail(email)):
        new_chofer = Personal(nombre, apellido, email, telefono, password)
        new_chofer.save()
        flash ("Alta chofer exitoso", "success")
        return redirect(url_for("listado_chofer"))
    else: 
        if not (validarPassword(password)):
            flash ("Contraseña corta", "error")
            return redirect(url_for("render_alta_chofer"))
        else:
            flash ("Email registrado en el sistema", "error")
            return redirect(url_for("render_alta_chofer")) 

def editar_perfil_personal(id):
    verificarSesionChofer()
    chofer = Personal.buscarChoferPorId(id)
    datos= request.form
    if (chofer.email != datos["email"]):
        if (validarPassword(datos["password"]) and validarEmail(datos["email"])):
            chofer.nombre = datos["nombre"]
            chofer.apellido = datos["apellido"]
            chofer.email = datos["email"]
            chofer.telefono = datos["telefono"]
            chofer.password = datos["password"]
            Personal.actualizar(chofer)
            flash ("Datos de chofer actualizados exitosamente", "success")
            return redirect(url_for("ver_perfil_personal"))
        else: 
            if not (validarPassword(datos["password"])):
                flash ("Contraseña corta", "error")
                return render_template("personal/editPerfilPersonal.html", chofer = chofer)
            else:
                flash ("Email registrado en el sistema", "error")
                return render_template("personal/editPerfilPersonal.html", chofer = chofer)  
    else:
            if (validarPassword(datos["password"])):
                chofer.nombre = datos["nombre"]
                chofer.apellido = datos["apellido"]
                chofer.telefono = datos["telefono"]
                chofer.password = datos["password"]
                Personal.actualizar(chofer)
                flash ("Datos de chofer actualizados exitosamente", "success")
                return redirect(url_for("ver_perfil_personal"))
            else:
                flash ("Contraseña corta", "error")
                return render_template("personal/editPerfilPersonal.html", chofer = chofer)        

def editar_chofer(id):
    verificarSesionAdmin()
    chofer = Personal.buscarChoferPorId(id)
    datos = request.form
    if (chofer.email != datos["email"]):
        if (validarPassword(datos["password"]) and validarEmail(datos["email"])):
            chofer.nombre = datos["nombre"]
            chofer.apellido = datos["apellido"]
            chofer.email = datos["email"]
            chofer.telefono = datos["telefono"]
            chofer.password = datos["password"]
            Personal.actualizar(chofer)
            flash ("Datos de chofer actualizados exitosamente", "success")
            return redirect(url_for("listado_chofer"))
        else: 
            if not (validarPassword(datos["password"])):
                flash ("Contraseña corta", "error")
                return render_template("personal/editChofer.html", chofer = chofer)
            else:
                flash ("Email registrado en el sistema", "error")
                return render_template("personal/editChofer.html", chofer = chofer)  
    else:
            if (validarPassword(datos["password"])):
                chofer.nombre = datos["nombre"]
                chofer.apellido = datos["apellido"]
                chofer.telefono = datos["telefono"]
                chofer.password = datos["password"]
                Personal.actualizar(chofer)
                flash ("Datos de chofer actualizados exitosamente", "success")
                return redirect(url_for("listado_chofer"))
            else:
                flash ("Contraseña corta", "error")
                return render_template("personal/editChofer.html", chofer = chofer)

def devolvelEmail():
    #Devuelve los email de todos los choferes 
    aux = listaChoferes()
    listaEmails =[]
    print (type(aux))
    for a in aux:
        listaEmails.append(a.email)
    return listaEmails    

def validarEmail(email):
    #Valida que no exista en la tabla chofer el email que llego por parametro 
    aux = devolvelEmail()
    if email in aux:
        return False
    return True

def eliminar_chofer(id):
    chofer = Personal.buscarChoferPorId(id)
    if (len(chofer.combis) == 0):
        flash ("Baja de chofer exitoso", "success")
        Personal.eliminar_chofer(chofer)
    else:
        flash ("El chofer tiene una combi asignada, por favor realize las operaciones necesarias y vuelve a intentarlo", "error")
    return redirect (url_for("listado_chofer"))

def nombreCompleto():
    return Personal.nombre()

def render_viajesPendientes_chofer():
    verificarSesionChofer()
    chofer = Personal.buscarChoferPorId(session['id'])
    combis = chofer.combis
    rutas = []
    for each in combis:
        aux = Ruta.buscarPorCombi(each.id)   
        for x in aux:
            rutas.append(x)
    viajes = []
    for each in rutas:
        aux = Viaje.buscarPorRuta(each.id)
        for x in aux:
            viajes.append(x)
    proxPost=[]
    prox_viaje = devolverUltimoViaje(viajes)
    if (devolverUltimoViaje(viajes) != None):
        boletos = Boleto.buscarBoletoPorIdViajeYPendiente(prox_viaje.id)
        proxPost.append({
            'id':prox_viaje.id,
            'origen': Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(prox_viaje.id_ruta).id_origen).localidad,
            'destino': Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(prox_viaje.id_ruta).id_destino).localidad,
            'asientos': prox_viaje.asientos_disponibles,
            'fecha': prox_viaje.fecha,
            'horaSalida': prox_viaje.horaSalida,
            'horaLlegada': prox_viaje.horaLlegada,
            'asientosVendidos': prox_viaje.asientos - prox_viaje.asientos_disponibles,
            'estado': prox_viaje.estado,
            'tienePasajeros': boletos.count(),
            'paso': prox_viaje.paso
        })
    viajePost=[]
    for each in viajes:
        if each.enabled == 1 and (each.estado == 1 or each.estado == 2):
            boletos = Boleto.buscarBoletoPorIdViajeYPendiente(each.id)
            if (each.id != prox_viaje.id):
                viajePost.append({
                    'id':each.id,
                    'origen': Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(each.id_ruta).id_origen).localidad,
                    'destino': Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(each.id_ruta).id_destino).localidad,
                    'asientos': each.asientos_disponibles,
                    'fecha': each.fecha,
                    'horaSalida': each.horaSalida,
                    'horaLlegada': each.horaLlegada,
                    'asientosVendidos': each.asientos - each.asientos_disponibles,
                    'estado': each.estado,
                    'tienePasajeros': boletos.count(),
                    'paso': each.paso
                })
    if (len(viajePost) == 0) and (len(proxPost) == 0):
        flash("No tienes proximos viajes", "warning")
    if len(proxPost) > 0:
        return render_template('personal/listado_viajes_chofer.html', viajes = viajePost, viene = 1, prox = proxPost[0], ok = True)
    else:
        return render_template('personal/listado_viajes_chofer.html', viajes = viajePost, viene = 1, prox = proxPost, ok = False)

def devolverUltimoViaje(viajes):
    viaje_prox = None
    fecha_prox = datetime.strptime("8000-01-01", "%Y-%m-%d")
    for each in viajes:
        if (each.estado == 1 or each.estado == 2) and (each.enabled == 1):
            fecha = datetime.strptime(str(str(each.fecha)), "%Y-%m-%d")
            if (fecha <= fecha_prox):
                viaje_prox = each
                fecha_prox = fecha
    return viaje_prox

def render_viajesFinalizados_chofer():
    verificarSesionChofer()
    chofer = Personal.buscarChoferPorId(session['id'])
    combis = chofer.combis
    rutas = []
    for each in combis:
        aux = Ruta.buscarPorCombi(each.id)   
        for x in aux:
            rutas.append(x)
    viajes = []
    for each in rutas:
        aux = Viaje.buscarPorRuta(each.id)   
        for x in aux:
            viajes.append(x)
    viajePost=[]
    for each in viajes:
        if each.enabled == 1 and each.estado == 3:
            viajePost.append({
                'id':each.id,
                'origen': Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(each.id_ruta).id_origen).localidad,
                'destino': Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(each.id_ruta).id_destino).localidad,
                'asientos': each.asientos_disponibles,
                'fecha': each.fecha,
                'horaSalida': each.horaSalida,
                'horaLlegada': each.horaLlegada,
                'estado': each.estado
            })
    if len(viajePost) == 0:
        flash("No hemos registrado viajes finalizados para usted", "warning")
    return render_template('personal/listado_viajes_chofer.html', viajes = viajePost, viene = 2)

def confirmar_datos_covid(idP, idV):
    datos = request.form
    temperatura = datos["temperatura"]
    sintomas = 0
    pasajeroPost = []
    if(38 <= int(temperatura)):
        boleto = Boleto.buscarBoletoPorIdViajeIdCliente(idV, idP)
        boleto.estado = 5
        Boleto.actualizar(boleto)
        vendidos = Boleto.buscarBoletoPorIdViaje(idV)
        for vendido in vendidos:
            if (vendido.estado != 4):
                pasajeroPost.append({
                    "id": vendido.id_cliente,
                    "nombre": Cliente.buscarPorId(vendido.id_cliente).nombre,
                    "apellido": Cliente.buscarPorId(vendido.id_cliente).apellido,
                    "email": Cliente.buscarPorId(vendido.id_cliente).email,
                    "estado": vendido.estado   
                })
        return render_template("personal/listaPasajeros.html", pasajeros = pasajeroPost, idv = idV)
    if(request.form.get('fiebre') == 'isTrue'):
        sintomas += 1
    if(request.form.get('perdida_gusto_olfato') == 'isTrue'):
        sintomas += 1
    if(request.form.get('dolor_garganta') == 'isTrue'):
        sintomas += 1
    if(request.form.get('problemas_respiratorios') == 'isTrue'):
        sintomas += 1
    if(request.form.get('dolor_cabeza') == 'isTrue'):
        sintomas += 1
    if(sintomas >= 2):
        boleto = Boleto.buscarBoletoPorIdViajeIdCliente(idV, idP)
        boleto.estado = 5
        Boleto.actualizar(boleto)
        vendidos = Boleto.buscarBoletoPorIdViaje(idV)
        for vendido in vendidos:
            if (vendido.estado != 4):
                pasajeroPost.append({
                    "id": vendido.id_cliente,
                    "nombre": Cliente.buscarPorId(vendido.id_cliente).nombre,
                    "apellido": Cliente.buscarPorId(vendido.id_cliente).apellido,
                    "email": Cliente.buscarPorId(vendido.id_cliente).email,
                    "estado": vendido.estado   
                })
        return render_template("personal/listaPasajeros.html", pasajeros = pasajeroPost, idv = idV, aceptado = 0)
    else:
        vendidos = Boleto.buscarBoletoPorIdViaje(idV)
        for vendido in vendidos:
            if (vendido.estado != 4):
                pasajeroPost.append({
                    "id": vendido.id_cliente,
                    "nombre": Cliente.buscarPorId(vendido.id_cliente).nombre,
                    "apellido": Cliente.buscarPorId(vendido.id_cliente).apellido,
                    "email": Cliente.buscarPorId(vendido.id_cliente).email,
                    "estado": vendido.estado   
                })
        return render_template("personal/listaPasajeros.html", pasajeros = pasajeroPost, idv = idV, aceptado = 1)
def reporteCOVID():
    verificarSesionAdmin()
    boletos = Boleto.all()
    reportePost = []
    for each in boletos:
        if each.estado == 5:
            reportePost.append({
                'nombre': Cliente.buscarPorId(each.id_cliente).nombre,
                'apellido': Cliente.buscarPorId(each.id_cliente).apellido,
                'email': Cliente.buscarPorId(each.id_cliente).email,
                'origen': Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(Viaje.buscarViajePorId(each.id_viaje).id_ruta).id_origen).localidad,
                'destino': Lugar.buscarLugarPorId(Ruta.buscarRutaPorId(Viaje.buscarViajePorId(each.id_viaje).id_ruta).id_destino).localidad,
                'fecha': Viaje.buscarViajePorId(each.id_viaje).fecha
            })
    if len(reportePost) == 0:
        flash("No hay pasajeros rechazados por sintomas", "warning")    
    return render_template("personal/reporte.html", reportes=reportePost)
