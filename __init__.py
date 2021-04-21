from flask import Flask, render_template
from resources import usuario

app = Flask (__name__)


app.add_url_rule("/register", "userRegister", usuario.userRegister)

@app.route('/')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)