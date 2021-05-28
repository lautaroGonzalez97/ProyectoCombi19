from flask import render_template, session, redirect, url_for, flash, request, abort
from helpers.auth import authenticated
from models.combi import Combi
from models.personal import Personal
from resources.personal import verificarSesionAdmin 


def render_alta_combi():
    verificarSesionAdmin()
    personal = Personal.all()
    choferes = list (filter(lambda x: x.tipo == 2, personal))
    tipos_asiento=['SemiCama', 'Cama']
    return render_template("combi/addCombi.html", choferes = choferes, tipos = tipos_asiento)

def render_editar_combi(id):
    verificarSesionAdmin()
    combi = Combi.buscarCombiPorId(id)
    personal = Personal.all()
    choferes = list (filter(lambda x: x.tipo == 2, personal))
    tipos_asiento=['SemiCama', 'Cama']
    return render_template("combi/editCombi.html", combi = combi, choferes = choferes, tipos = tipos_asiento)

def listado_combis(): 
    verificarSesionAdmin()
    combis = Combi.all()
    combisPost=[]
    for each in combis:
        combisPost.append({
            'id':each.id,
            'patente':each.patente,
            'modelo':each.modelo,
            'asientos':each.asientos,
            'tipo':each.tipo,
            'id_chofer': Personal.buscarChoferPorId(each.id_chofer).email 
        })
    if len(combis) == 0:
        flash ("No hay combis cargadas", "warning")
    return render_template("combi/listaCombis.html", combis = combisPost)

def alta_combi():
    datos = request.form
    patente = datos["patente"]
    modelo = datos["modelo"]
    asientos = datos["asientos"]
    tipo = datos["tipos"]
    chofer = datos["choferes"]
    if (evaluarPatente(patente)):
        new_combi = Combi(patente, modelo, asientos, tipo, chofer)
        new_combi.save()
        flash ("Alta de combi exitoso", "success")
        return redirect(url_for("listado_combis"))
    else:
        flash ("Patente cargada en el sistema", "error")  
        return redirect(url_for("render_alta_combi")) 

def devolverPatentes():
    aux = Combi.all()
    patentes=[]
    for c in aux:
        patentes.append(c.patente)
    return patentes

def evaluarPatente(patente):
    aux = devolverPatentes()
    if (patente in aux):
        return False
    return True

def editar_combi(id):
    verificarSesionAdmin()
    combi = Combi.buscarCombiPorId(id)
    datos = request.form
    if (combi.patente != datos["patente"]):
        if (evaluarPatente(datos["patente"])):
            combi.patente = datos["patente"]
            combi.modelo = datos["modelo"]
            combi.asientos = datos["asientos"]
            combi.tipo = datos["tipos"]
            combi.id_chofer = datos["choferes"] #falta arreglar esta verificacion, no queda bien el edit cuando se edita con una patente que ya existe
            Combi.actualizar(combi)
            flash ("Datos de la combi actualizados", "success")
            return redirect(url_for("listado_combis"))
        else:
            personal = Personal.all()
            choferes = list (filter(lambda x: x.tipo == 2, personal))
            flash ("Patente cargada de sistema", "error")
            tipos_asientos= ["SemiCama", "Cama"] 
            return render_template("combi/editCombi.html", combi = combi, choferes = choferes, tipos= tipos_asientos)
    else:
        combi.modelo = datos["modelo"]
        combi.asientos = datos["asientos"]
        combi.tipo = datos["tipos"]
        combi.id_chofer = datos["choferes"] #falta arreglar esta verificacion, no queda bien el edit cuando se edita con una patente que ya existe
        Combi.actualizar(combi)
        flash ("Datos de la combi actualizados", "success")
        return redirect(url_for("listado_combis"))
    
def eliminar_combi(id):
    combi = Combi.buscarCombiPorId(id)
    if (len(combi.rutas) == 0):
        flash ("Baja de combi exitoso", "success")
        Combi.eliminar_combi(combi)       
    else:
        flash("La combi tiene asignada al menos una ruta de viaje, por favor realice las operaciones necesarias y vuelva a intentarlo", "error")
    return redirect(url_for("listado_combis"))