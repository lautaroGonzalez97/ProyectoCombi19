from flask import Flask, render_template

def login():
    return render_template("login.html")