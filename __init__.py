from flask import Flask, render_template, redirect, url_for
from resources import usuario

app = Flask (__name__)

#Usuarios
app.add_url_rule("/login", "login", usuario.login)

@app.route('/')
def home():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)