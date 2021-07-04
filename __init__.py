from flask import Flask, render_template, redirect, url_for, session, request, flash
#para trabajar fechas
from datetime import datetime
from dateutil.relativedelta import relativedelta #pip install python-dateutil
#base de datos
from flask_mysqldb import MySQL
import db
#funcionalidades
from resources import cliente, personal, insumo, combi, tarjeta, lugar, ruta, viaje, comentario, boleto
from helpers.auth import authenticated 

app = Flask (__name__)
app.config["DB_HOST"] = "localhost"
app.config["DB_USER"] = "root"
app.config["DB_PASS"] = ""
app.config["DB_NAME"] = "combi_19"
mysql = MySQL(app)

#Configure db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+app.config["DB_USER"] + \
        ':'+app.config["DB_PASS"]+'@' + \
        app.config["DB_HOST"]+'/'+app.config["DB_NAME"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_db(app)

app.secret_key = 'esto-es-una-clave-muy-secreta'

#Rutas Clientes
app.add_url_rule("/crear_cliente", "crear_cliente", cliente.crear, methods=["POST"])
app.add_url_rule("/registrar_cliente", "render_altaCliente", cliente.registrar)
app.add_url_rule("/autenticar_cliente", "autenticar_cliente", cliente.autenticar, methods=["POST"])
app.add_url_rule("/login_cliente", "login_cliente", cliente.login)
app.add_url_rule("/logout_cliente", "logOut_cliente", cliente.logOut)
app.add_url_rule("/editar_cliente/<id>", "render_editar_cliente", cliente.render_editar_cliente)
app.add_url_rule("/saveEdit_cliente/<id>", "editar_cliente", cliente.editar_cliente, methods=["POST"])
app.add_url_rule("/home_cliente", "home_cliente", cliente.home)
app.add_url_rule ("/ver_perfil", "ver_perfil", cliente.ver_perfil)  
app.add_url_rule("/busqueda", "busqueda", cliente.busqueda, methods=["POST"]) 
    #---acciones comprar viaje---
app.add_url_rule("/detalle_viaje/<id>", "render_comprar_viaje", boleto.render_comprar_viaje) 
app.add_url_rule("/compra_viaje/<id>", "comprar_viaje", boleto.comprar_viaje, methods=["POST"]) 
app.add_url_rule("/cancelar_viaje/<id>", "cancelar_viaje", boleto.cancelar_viaje)
app.add_url_rule("/pago_con_Tarjeta/<id>/<boletos>", "pagar_con_tarjeta", boleto.pagar_con_tarjeta, methods=["POST"]) 
    #---acciones ver viajes proximos---
app.add_url_rule ("/ver_mis_viajes", "ver_mis_viajes", cliente.ver_mis_viajes)  
    #---acciones comentarios---
app.add_url_rule ("/listado_misComentarios", "listado_misComentarios", comentario.listado_misComentarios)
app.add_url_rule("/save_comentario/<id>", "alta_comentario", comentario.alta_comentario, methods=["POST"])
app.add_url_rule("/editar_comentario/<id>", "render_editar_comentario", comentario.render_editar_comentario)
app.add_url_rule("/saveEdit_comentario/<id>", "editar_comentario", comentario.editar_comentario, methods=["POST"])
app.add_url_rule("/eliminar_comentario/<id>", "eliminar_comentario", comentario.eliminar_comentario)
#Rutas Tarjeta
app.add_url_rule("/tarjeta_cliente/<nom>/<ape>/<email>/<nac>/<contra>", "crear_tarjeta", tarjeta.crear, methods=["POST"])
app.add_url_rule("/eliminar_tarjeta/<id>", "eliminar_tarjeta", tarjeta.eliminar_tarjeta)
app.add_url_rule("/editar_tarjeta/<id>", "render_editar_tarjeta", tarjeta.render_editar_tarjeta)
app.add_url_rule("/saveEdit_tarjeta/<id>", "editar_tarjeta", tarjeta.editar_tarjeta, methods=["POST"])
#Rutas Personal
app.add_url_rule("/login_personal", "autenticar_personal", personal.autenticar, methods=["POST"])
app.add_url_rule("/login_personal", "login_personal", personal.login)
app.add_url_rule("/logout_personal", "logOut_personal", personal.logOut)
app.add_url_rule("/home_chofer", "home_chofer", personal.home_chofer)
app.add_url_rule("/render_viajesPendientes_chofer", "render_viajesPendientes_chofer", personal.render_viajesPendientes_chofer)
app.add_url_rule("/render_viajesFinalizados_chofer", "render_viajesFinalizados_chofer", personal.render_viajesFinalizados_chofer)

#Rutas Admin
app.add_url_rule("/home_admin", "home_admin", personal.home_admin)
    #---acciones chofer---
app.add_url_rule("/listado_choferes", "listado_chofer", personal.listado_chofer)
app.add_url_rule("/alta_chofer", "render_alta_chofer", personal.render_alta_chofer)
app.add_url_rule("/save_chofer", "alta_chofer", personal.alta_chofer, methods=["POST"])
app.add_url_rule("/editar_chofer/<id>", "render_editar_chofer", personal.render_editar_chofer)
app.add_url_rule("/saveEdit_chofer/<id>", "editar_chofer", personal.editar_chofer, methods=["POST"])
app.add_url_rule("/eliminar_chofer/<id>", "eliminar_chofer", personal.eliminar_chofer)
app.add_url_rule ("/ver_perfilPersonal", "ver_perfil_personal", personal.ver_perfil_personal) 
app.add_url_rule("/saveEdit_perfil/<id>", "editar_perfil_personal", personal.editar_perfil_personal, methods=["POST"])   
    #---acciones insumos---
app.add_url_rule("/listado_insumos", "listado_insumos", insumo.listado_insumos)
app.add_url_rule("/alta_insumo", "render_alta_insumo", insumo.render_alta_insumo)
app.add_url_rule("/save_insumo", "alta_insumo", insumo.alta_insumo, methods=["POST"])
app.add_url_rule("/editar_insumo/<id>", "render_editar_insumo", insumo.render_editar_insumo)
app.add_url_rule("/saveEdit_insumo/<id>", "editar_insumo", insumo.editar_insumo, methods=["POST"])
app.add_url_rule("/eliminar_insumo/<id>", "eliminar_insumo", insumo.eliminar_insumo)
    #---acciones combi---
app.add_url_rule("/listado_combis", "listado_combis", combi.listado_combis)
app.add_url_rule("/alta_combi", "render_alta_combi", combi.render_alta_combi)
app.add_url_rule("/save_combi", "alta_combi", combi.alta_combi, methods=["POST"])
app.add_url_rule("/editar_combi/<id>", "render_editar_combi", combi.render_editar_combi)
app.add_url_rule("/saveEdit_combi/<id>", "editar_combi", combi.editar_combi, methods=["POST"])
app.add_url_rule("/eliminar_combi/<id>", "eliminar_combi", combi.eliminar_combi)
    #---acciones lugar---
app.add_url_rule("/listado_lugares", "listado_lugares", lugar.listado_lugares)
app.add_url_rule("/alta_lugar", "render_alta_lugar", lugar.render_alta_lugar)
app.add_url_rule("/save_lugar", "alta_lugar", lugar.alta_lugar, methods=["POST"])
app.add_url_rule("/editar_lugar/<id>", "render_editar_lugar", lugar.render_editar_lugar)
app.add_url_rule("/saveEdit_lugar/<id>", "editar_lugar", lugar.editar_lugar, methods=["POST"])
app.add_url_rule("/eliminar_lugar/<id>", "eliminar_lugar", lugar.eliminar_lugar)
    #---acciones ruta---
app.add_url_rule("/listado_rutas", "listado_rutas", ruta.listado_rutas) 
app.add_url_rule("/alta_ruta", "render_alta_ruta", ruta.render_alta_ruta)
app.add_url_rule("/save_ruta", "alta_ruta", ruta.alta_ruta, methods=["POST"])
app.add_url_rule("/editar_ruta/<id>", "render_editar_ruta", ruta.render_editar_ruta)
app.add_url_rule("/saveEdit_ruta/<id>", "editar_ruta", ruta.editar_ruta, methods=["POST"])
app.add_url_rule("/eliminar_ruta/<id>", "eliminar_ruta", ruta.eliminar_ruta)
    #---acciones viaje---
app.add_url_rule("/listado_viajes", "listado_viajes", viaje.listado_viajes) 
app.add_url_rule("/alta_viaje", "render_alta_viaje", viaje.render_alta_viaje)
app.add_url_rule("/save_viaje", "alta_viaje", viaje.alta_viaje, methods=["POST"])
app.add_url_rule("/editar_viaje/<id>", "render_editar_viaje", viaje.render_editar_viaje)
app.add_url_rule("/saveEdit_viaje/<id>", "editar_viaje", viaje.editar_viaje, methods=["POST"])
app.add_url_rule("/eliminar_viaje/<id>", "eliminar_viaje", viaje.eliminar_viaje)

def home ():
    if ("id" not in session):
        return redirect(url_for("login_cliente"))
    return redirect(url_for("home_cliente"))

app.add_url_rule("/", "home", home)

if __name__ == '__main__':
    app.run(port= 8080, debug=True)




