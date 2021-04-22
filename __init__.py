from flask import render_template, redirect, url_for, session
from resources import usuario

app = Flask (__name__)

#Usuarios
app.add_url_rule("/iniciar_sesion","login", usuario.login)
app.add_url_rule("/autenticacion", "autenticar_login", usuario.autenticar, methods=["POST"])
app.add_url_rule("/cerrar_sesion", "logout", usuario.logout)

#Esto es para cuando ingresan a la pagina, si su id no esta en Session los tira al template login, sino entran a la pagina (#)
@app.route('/')
def home():
    if (not 'id' in session):
        return redirect(url_for("login"))
    return redirect(url_for('#')) #redirije a home

if __name__ == '__main__':
    app.run(debug=True)