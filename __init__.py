from flask import Flask, render_template, redirect, url_for, session, request, flash
#para trabajar fechas
from datetime import datetime
from dateutil.relativedelta import relativedelta #pip install python-dateutil
#base de datos
from flask_mysqldb import MySQL
import db
#funcionalidades
from resources import cliente, personal, insumo, combi, tarjeta, lugar, ruta
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
app.add_url_rule("/home_cliente", "home_cliente", cliente.home)

#Rutas Tarjeta
app.add_url_rule("/tarjeta_cliente/<nom>/<ape>/<email>/<nac>/<contra>", "crear_tarjeta", tarjeta.crear, methods=["POST"])

#Rutas Personal
app.add_url_rule("/login_personal", "autenticar_personal", personal.autenticar, methods=["POST"])
app.add_url_rule("/login_personal", "login_personal", personal.login)
app.add_url_rule("/logout_personal", "logOut_personal", personal.logOut)
app.add_url_rule("/home_chofer", "home_chofer", personal.home_chofer)

#Rutas Admin
app.add_url_rule("/home_admin", "home_admin", personal.home_admin)
    #---acciones chofer---
app.add_url_rule("/listado_choferes", "listado_chofer", personal.listado_chofer)
app.add_url_rule("/alta_chofer", "render_alta_chofer", personal.render_alta_chofer)
app.add_url_rule("/save_chofer", "alta_chofer", personal.alta_chofer, methods=["POST"])
app.add_url_rule("/editar_chofer/<id>", "render_editar_chofer", personal.render_editar_chofer)
app.add_url_rule("/saveEdit_chofer/<id>", "editar_chofer", personal.editar_chofer, methods=["POST"])
app.add_url_rule("/eliminar_chofer/<id>", "eliminar_chofer", personal.eliminar_chofer)
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
#falta eliminar una combi
    #---acciones lugar---
app.add_url_rule("/listado_lugares", "listado_lugares", lugar.listado_lugares)
app.add_url_rule("/alta_lugar", "render_alta_lugar", lugar.render_alta_lugar)
app.add_url_rule("/save_lugar", "alta_lugar", lugar.alta_lugar, methods=["POST"])
app.add_url_rule("/editar_lugar/<id>", "render_editar_lugar", lugar.render_editar_lugar)
app.add_url_rule("/saveEdit_lugar/<id>", "editar_lugar", lugar.editar_lugar, methods=["POST"])
#falta eliminar un lugar
    #---acciones ruta---
app.add_url_rule("/listado_rutas", "listado_rutas", ruta.listado_rutas) 
app.add_url_rule("/alta_ruta", "render_alta_ruta", ruta.render_alta_ruta)
app.add_url_rule("/save_ruta", "alta_ruta", ruta.alta_ruta, methods=["POST"])

def home ():
    if ("id" not in session):
        return redirect(url_for("login_cliente"))
    return redirect(url_for("home_cliente"))

app.add_url_rule("/", "home", home)

if __name__ == '__main__':
    app.run(port= 8080, debug=True)




