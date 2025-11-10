from flask import (render_template,request,redirect,url_for,flash,abort,jsonify,session)
import math
import time
import requests
import hashlib
from src.database import engine
from sqlalchemy.orm import sessionmaker, scoped_session
from src.Model.models import (Usuario,Reserva,Quarto,Hospede,Tipo_de_quarto)
from werkzeug.security import generate_password_hash, check_password_hash
import re
from src import app


SessionLocal = scoped_session(sessionmaker(bind=engine))

mykey = hashlib.sha256()

def isEmailValid(email):
    regex = r"^[a-zA-Z.-]+@[a-zA-Z]+\.[a-z]{2,}$"
    print(f"Email: {email}")
    return bool(re.fullmatch(regex,email))


def findReservaByUserId(id):
   return None

def roomsByNameId(id):
    return none

    

def login(completeName):
   
    return None

def fetchGithubImg(githubProfile):
    try:
        res = requests.get(f"https://api.github.com/users/{githubProfile}")
        data = res.json()
        return data['avatar_url']
    except:
        return None
    
@app.route("/", methods=["POST","GET"])
def index():
    method = request.method
    if method == "POST":
        form = request.form
        name = form.get("username")
        print(name)
        img = fetchGithubImg(name)
        print(img)
        user = login(name)
        if (user):

            password = form.get("password")
            print(f"Email valid: {isEmailValid(user.email)}")
            reservasbyname = findReservaByUserId(user.id_guest)
            rooms = roomsByNameId(user.id_guest) 
            return render_template("guest.html",user=user,password=password,profilePic = img,rooms=rooms)


    return render_template("index.html")

@app.route("/register",methods=["POST","GET"])
def register():
    db = SessionLocal()
    if request.method == "POST":
        nome = request.form.get("fullname")
        email = request.form.get("email")
        senha = request.form.get("password")
        novo_usuario = Usuario(nome_completo = nome,
                               email = email, senha_hash = generate_password_hash(senha))
        db.add(novo_usuario)
        db.commit()
        return render_template("register.html") 
    return render_template("register.html") 