from flask import Flask, render_template, redirect, url_for
from resources import usuario

app = Flask (__name__)

#Usuarios
#app.add_url_rule("/login", "login", usuario.login)
#app.add_url_rule("/register", "register", usuario.register)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
   return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/Contacto')
def contacto():
    return render_template('contacto.html')

if __name__ == '__main__':
    app.run(debug=True)