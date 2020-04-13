from flask import Flask, render_template, request, redirect, url_for, jsonify

from flask_cors import CORS
from bson import ObjectId
from pymongo import MongoClient
import os
import logging
import json
from bson import json_util
from azure.storage.queue import QueueService
from Producto import Producto
from Orden import Orden
from Ingrediente import Ingrediente
from Busqueda import Busqueda
from queue_messages import QueueWorker

app = Flask(__name__)
title = "Monjosh App"
heading = "Monjosh App"


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='example.log')

# Conexion con API de MongoDB de Cosmos
client = MongoClient("mongodb://monjoshdb:2PBsBQi43gAKECaFF8A1bYrQeEHxVUrllDN82V8T3gcTrOsPFT6TqeHdqHyNXJbDoYOWorosspRW2pXrT8YVlQ==@monjoshdb.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@monjoshdb@")  # host uri
db = client.monjoshdb
db.authenticate(name="monjoshdb",
                password='2PBsBQi43gAKECaFF8A1bYrQeEHxVUrllDN82V8T3gcTrOsPFT6TqeHdqHyNXJbDoYOWorosspRW2pXrT8YVlQ==')
queue_service = QueueService(account_name='joshstoragequeue', account_key='AhaC+CI57J5fz17mFen4sFNP/KawQMKGUAaAPhjgoJtarr5tQ4z/3VP0/Qc5zUBNV/9FvM4aZPMbSZbFihwYBQ==')

# Nombre de colecciones
busquedasCollection = db.busquedas
ordenesCollection = db.ordenes


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
    mensaje_enviado = queue_messages.queue_busqueda("query=" + query)
    if mensaje_enviado:
        logging.info(f'Busqueda enviada a FoodApi')
        return 'Busqueda enviada a FoodApi'
    else:
        logging.info(f'Error al enviar mensaje en el queue')
        return "Error en el servidor", 500


@app.route("/busqueda", methods=['POST'])
def registrarBusqueda(producto):
    try:
        busqueda = Busqueda(producto)
        busquedasCollection.insert(
            {
                'producto': busqueda.producto,
                'fecha': busqueda.fecha,
                'puntos': busqueda.puntos,
            }
        )
        return 'busqueda registrada'
    except Exception as exc:
        logging.error(f'ERROR: No se pudo registrar busqueda: {exc}')
        return 'busqueda no registrada'


@app.route("/busquedas/all", methods=['GET'])
def listaBusquedas():
    try:
        logging.info(f'INICIO ==> OBTENER TODAS LAS BUSQUEDAS')

        busquedas = [busqueda for busqueda in busquedasCollection.find()]
        busquedas_json = json.loads(json_util.dumps(busquedas))

        logging.info(f'FIN ==> OBTENER TODAS LAS BUSQUEDAS')

        return jsonify({'busquedas': busquedas_json})
    except Exception as exc:
        logging.error(f'ERROR: No se pueden obtener las busquedas: {exc}')
        return None


@app.route("/enviarMensaje", methods=['GET'])
def enviarMensajeACola():
    queue_service.create_queue('monjoshqueue')
    queue_service.put_message('monjoshqueue', u'Hello Monica')
    return 'mensaje enviado'


@app.route("/generarOrden", methods=['POST'])
def generarOrden():
    request_json = request.get_json()
    numero_orden = request_json.get('numeroOrden')
    fecha = request_json.get('fecha')
    estado = request_json.get('estado')
    precio = request_json.get('precio')
    productos = request_json.get('productos')
    lst_productos = []
    for producto in productos:
        ingredientes = producto['ingredientes']
        lst_ingredientes = []
        for ingrediente in ingredientes:
            i = Ingrediente(
                nombre_ingrediente=ingrediente['nombreIngrediente'],
                cantidad_ingrediente=ingrediente['cantidadIngrediente'],
                precio_ingrediente=ingrediente['precioIngrediente']
            )
            ingrediente_json = json.dumps(i, default=i.ingredienteADiccionario)
            lst_ingredientes.append(ingrediente_json)

        ing_objects = [json.loads(ing) for ing in lst_ingredientes]
        p = Producto(
            producto['nombreProducto'],
            producto['cantidadProducto'],
            producto['precioProducto'],
            ing_objects
        )
        producto_json = json.dumps(p, default=p.productoADiccionario)
        lst_productos.append(producto_json)

    orden = Orden(
        numero_orden,
        fecha,
        estado,
        precio,
        lst_productos
    )
    prod_objects = [json.loads(prod) for prod in orden.productos]
    ordenesCollection.insert_one(
        {
            'numeroOrden': orden.numero_orden,
            'fecha': orden.fecha,
            'estado': orden.estado,
            'precio': orden.precio,
            'productos': prod_objects
        }
    )
    return 'Orden generada'


@app.route("/ordenes/all", methods=['GET'])
def listaOrdenes():
    try:
        logging.info(f'INICIO ==> OBTENER TODAS LAS ORDENES')

        ordenes = [orden for orden in ordenesCollection.find()]
        ordenes_json = json.loads(json_util.dumps(ordenes))

        logging.info(f'FIN ==> OBTENER TODAS LAS ORDENES')

        return jsonify({'ordenes': ordenes_json})
    except Exception as exc:
        logging.error(f'ERROR: No se pueden obtener las busquedas: {exc}')
        return None


@app.route("/ordenes/<estado>", methods=['GET'])
def listaOrdenesPorEstado(estado):
    try:
        logging.info(f'INICIO ==> OBTENER TODAS LAS ORDENES POR ESTADO')

        ordenes = [orden for orden in ordenesCollection.find({"estado": estado})]
        ordenes_json = json.loads(json_util.dumps(ordenes))

        logging.info(f'FIN ==> OBTENER TODAS LAS ORDENES POR ESTADO')

        return jsonify({'ordenes': ordenes_json})
    except Exception as exc:
        logging.error(f'ERROR: No se pueden obtener las busquedas: {exc}')
        return None


@app.route("/actualizarOrden", methods=['PUT'])
def actualizarOrden():
    try:
        request_json = request.get_json()
        id = request_json.get("_id")
        estado = request_json.get("estado")
        ordenesCollection.update({"_id": ObjectId(id)}, {'$set': {"estado": estado}})
        return 'Orden actualizada'
    except Exception as exc:
        logging.error(f'ERROR: No se pudo actualizar orden: {exc}')
        return 'Orden NO actualizada'


# APP.RUN y puerto
if __name__ == "__main__":
    app.run(debug=True, port=5000)
