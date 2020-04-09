from flask import Flask, render_template, request, redirect, url_for, jsonify
from bson import ObjectId
from pymongo import MongoClient
import os
import logging
import json
from bson import json_util
from queue_messages import QueueWorker
##from azure.storage.common import CloudStorageAccount

app = Flask(__name__)
title = "Monjosh App"
heading = "Monjosh App"

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='example.log')

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


@app.route('/buscar')
def buscar():
    # Possible arguments = query, diet, intolerances, includeIngredients, excludeIngredients,
    query = request.args.get("query")

    if query is None:
        return "Query no existente", 400

    logging.info(f'Realizando busqueda en queue de:', request.args)
    
    queue_messages = QueueWorker()
    mensaje_enviado = queue_messages.queue_busqueda("query="+query)
    if mensaje_enviado:
        logging.info(f'Busqueda enviada a FoodApi')
        return 'Busqueda enviada a FoodApi'
    else:
        logging.info(f'Error al enviar mensaje en el queue')
        return "Error en el servidor", 500 



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


@app.route("/ingredientes/all", methods=['GET'])
def listaIngredientes():
    try:
        logging.info(f'INICIO ==> OBTENER TODOS INGREDIENTES')
        
        ingredientes = ingredientesCollection.find()
        ingredientes_resultado = []
        for ingrediente in ingredientes:
            ingrediente.pop('_id')
            ingredientes_resultado.append(ingrediente)
            
        logging.info(f'FIN ==> OBTENER TODOS INGREDIENTES')

        return jsonify({'ingredientes': ingredientes_resultado})
    except Exception as exc:
        logging.error(f'ERROR: No se pueden obtener los ingredientes: {exc}')
        return None


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
