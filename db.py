import pymysql
from flask import current_app
from flask import g
from flask import cli

#SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    db.app = app
    from models import cliente, personal, tarjeta, insumo, combi, lugar, ruta, viaje
    db.create_all()


def connection():
    return db


def close(e=None):
    conn = g.pop("db_conn", None)

    if conn is not None:
        conn.close()