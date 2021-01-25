from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, redirect, session
from config.database import *
from commands.pmb import *
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = "rahasia"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        loginData = getLoginData(request.form["username"])
        password = request.form["password"]
        if loginData and check_password_hash(loginData["password"], password):
            session["user"] = loginData["nama"]
            return redirect(url_for("user"))
        else:
            flash("Email atau User Salah!")
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
@app.route('/user')
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))

app.run(host='0.0.0.0')