from flask import (render_template,request,redirect,url_for,flash,abort,jsonify,session)
import math
import time
import requests
import hashlib
import re
from src import app
from src.Model.guest import guests,Guest
from src.Model.reserva import reservas,Reserva
from src.Model.room import rooms,Room
mykey = hashlib.sha256()

def isEmailValid(email):
    regex = r"^[a-zA-Z.-]+@[a-zA-Z]+\.[a-z]{2,}$"
    print(f"Email: {email}")
    return bool(re.fullmatch(regex,email))


def findReservaByUserId(id):
    reservasByName = []
    for reserva in reservas:
        if reserva.id_hospede == id:
            reservasByName.append(reserva)

    return reservasByName

def roomsByNameId(id):
    reservasbyname = findReservaByUserId(id)
    print(f"Reservas por nome: {reservasbyname}")
    roomsbyid = []
    print(f"Reserva 1: {reservasbyname[0].numero_quarto}")
    roomsid = [reserva.numero_quarto for reserva in reservasbyname]
    print(f"Rooms por id {roomsid}")
    for room in rooms:
        if str(room.room_number) in str(roomsid):
            roomsbyid.append(room)

    print(roomsbyid)
    return roomsbyid

def login(completeName):
    print(completeName)
    for user in guests:
        if user.complete_name ==  completeName:
            return user
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