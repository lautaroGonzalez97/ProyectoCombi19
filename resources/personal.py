from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.personal import Personal

def verificarSesionChofer():
    if (not (authenticated(session)) or (not (session["tipo"] == "Chofer"))):
        abort(401)

def verificarSesionAdmin():
    if (not (authenticated(session)) or (not (session["tipo"] == "Admin"))):
        abort(401)

def home_chofer():
    verificarSesionChofer()
    return render_template("homeChofer.html")

def home_admin():
    verificarSesionAdmin()
    return render_template("homeAdmin.html")

def listado_chofer():
    verificarSesionAdmin()
    personal = Personal.all()
    choferes = list (filter(lambda x: x.tipo == 2, personal))
    if len(choferes) == 0:
        flash ("No hay choferes cargados", "warning")
    return render_template("listaChoferes.html", choferes = choferes)
    
def render_alta_chofer():
    verificarSesionAdmin()
    return render_template("addChofer.html")

def render_editar_chofer(id):
    verificarSesionAdmin()
    chofer = Personal.buscarChoferPorId(id)
    return render_template("editChofer.html", chofer = chofer)

def login():
    if (authenticated(session)):
        return redirect(url_for("home_personal"))
    return render_template("login_personal.html")

def logOut():
    if (authenticated(session)):
        del session["id"]
    return redirect(url_for("login_personal"))

def listaChoferes():
    personal = Personal.all()
    choferes = list (filter(lambda x: x.tipo == 2, personal))
    return choferes

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

def editar_chofer(id):
    verificarSesionAdmin()
    chofer = Personal.buscarChoferPorId(id)
    datos = request.form
    chofer.nombre = datos["nombre"]
    chofer.apellido = datos["apellido"]
    chofer.email = datos["email"]
    chofer.telefono = datos["telefono"]
    chofer.password = datos["password"]
    if (validarPassword(chofer.password) and validarEmail(chofer.email)):
        Personal.actualizar(chofer)
        flash ("Datos de chofer actualizados exitosamente", "success")
        return redirect(url_for("listado_chofer"))
    else: 
        if not (validarPassword(password)):
            flash ("Contraseña corta", "error")
            return render_template("editChofer.html", chofer = chofer)
        else:
            flash ("Email registrado en el sistema", "error")
            return render_template("editChofer.html", chofer = chofer)  

def devolvelEmail():
    """ 
    Devuelve los email de todos los choferes 
    """
    aux = listaChoferes()
    listaEmails =[]
    print (type(aux))
    for a in aux:
        listaEmails.append(a.email)
    return listaEmails    

def validarEmail(email):
    """ 
    Valida que no exista en la tabla chofer el email que llego por parametro 
    """
    aux = devolvelEmail()
    if email in aux:
        return False
    return True

def eliminar_chofer(id):
    chofer = Personal.buscarChoferPorId(id)
    print(chofer.nombre)
    print(chofer.combis)
    if (len(chofer.combis) == 0):
        print("NO TIENE COMBI")
        flash ("Baja de chofer exitoso", "success")
        Personal.eliminar_chofer(chofer)
    else:
        flash ("El chofer tiene una combi asignada, por favor realize las operaciones necesarias y vuelve a intentarlo", "error")
    return redirect (url_for("listado_chofer"))