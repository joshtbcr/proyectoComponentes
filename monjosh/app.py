from flask import Flask, render_template, request, redirect, url_for
from bson import ObjectId
from pymongo import MongoClient
import os

app = Flask(__name__)
title = "Monjosh App"
heading = "Monjosh App"

# Conexion con API de MongoDB de Cosmos
client = MongoClient("mongodb://monjoshdb:2PBsBQi43gAKECaFF8A1bYrQeEHxVUrllDN82V8T3gcTrOsPFT6TqeHdqHyNXJbDoYOWorosspRW2pXrT8YVlQ==@monjoshdb.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@monjoshdb@")  # host uri
db = client.monjoshdb
db.authenticate(name="monjoshdb",
                password='2PBsBQi43gAKECaFF8A1bYrQeEHxVUrllDN82V8T3gcTrOsPFT6TqeHdqHyNXJbDoYOWorosspRW2pXrT8YVlQ==')

# Nombre de colecciones
productosCollection = db.productos
ordenesCollection = db.ordenes
ingredientesCollection = db.ingredientes
usuariosCollection = db.usuarios

# Metodos RESTful
@app.route('/')
def hello():
    return 'Vista general'


@app.route("/ingrediente", methods=['POST'])
def ingresarIngrediente():
    nombre = "nombreIngredientePrueba"
    cantidad = "cantidadIngredientePrueba"
    ingredientesCollection.insert(
        {
            'nombre': nombre,
            'precio': cantidad
        }
    )
    return redirect("/")

##@app.route("/ingredientes/all", methods=['GET'])
##def listaIngredientes():
    ##lstingredientes = ingredientesCollection.find()
	##return jsonify()

@app.route("/producto", methods=['POST'])
def ingresarProducto():
    nombreProducto = "nombreProductoPrueba"
    precio = "precioProductoPrueba"
    productosCollection.insert(
        {
            'nombre': nombreProducto, 
            'precio': precio
        }
    )
    return redirect("/")


@app.route("/orden", methods=['POST'])
def ingresarOrden():
    numeroOrden = "nombreProductoPrueba"
    fecha = "precioProductoPrueba"
    estado = "precioProductoPrueba"
    precioOrden = "precioProductoPrueba"
    ordenesCollection.insert(
        {
            'numeroOrden': numeroOrden, 
            'fecha': fecha,
            'estado': estado, 
            'precio': precioOrden
        }
    )
    return redirect("/")


@app.route("/usuario", methods=['POST'])
def ingresarUsuario():
    username = "usernamePrueba"
    password = "passwordPrueba"
    email = "emailPrueba"
    usuariosCollection.insert(
        {
            "username": username, 
            "password": password, 
            "email": email
        }
    )
    return redirect("/")


# APP.RUN y puerto
if __name__ == "__main__":
    app.run(debug=True, port=5000)
