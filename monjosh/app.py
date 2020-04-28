from flask import Flask, render_template, request, redirect, url_for, jsonify

from flask_cors import CORS
from bson import ObjectId
from pymongo import MongoClient
import os
import logging
import json
import uuid
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

#Array de busquedas pendientes
busquedasPendientes = {}


# Metodos RESTful
@app.route('/')
def hello():
    return 'Vista general'


@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    try:
        # Possible arguments = query, diet, intolerances, includeIngredients, excludeIngredients,
        query = request.args.get("query")
        busquedaId = request.args.get("busquedaId")

        #Si es respuesta del FoodApi
        if request.method == 'POST':
            busquedasPendientes[busquedaId] = request.get_json()
            puntosDia = request.args.get("puntosDia")
            puntosBusqueda = request.args.get("puntosBusqueda")
            #Registrar busqueda


            return "Busqueda actualizada en WebApi"

        if request.method == 'GET':
            #Si es busqueda pendiente
            if query is None and busquedaId is not None:
                print("Procesando busqueda con ID= "+ busquedaId)
                
                print("Busquedas pendientes = ")
                for busquedaId, productos in busquedasPendientes.items():
                    if productos == False:
                        print("\tSin resolver = " + busquedaId)
                    else:
                        print("\tResuelta:  " + busquedaId)

                #Si la busqueda esta pendiente y ya fue resuelta por el FoodApi
                if busquedaId in busquedasPendientes and busquedasPendientes[busquedaId] != False:
                    productos = busquedasPendientes[busquedaId]
                    
                    #Eliminar de busquedas pendientes (quitar de RAM)
                    del busquedasPendientes[busquedaId]
                    #return jsonify(productos),200
                    return jsonify({'products': productos}),200
                    #return str(productos), 200

                #Si la busqueda esta pendiente pero no ha sido resuelta por el FoodApi
                elif busquedaId in busquedasPendientes and busquedaId == False:
                    return "Busqueda pendiente", 202
                else:
                    return "Busqueda inexistente", 404

            #Si es nueva busqueda del cliente
            elif query is not None:

                busquedaId = str(uuid.uuid4())
                busquedasPendientes[busquedaId] = False
                
                logging.info(f'Realizando busqueda en queue de:', request.args)

                queue_messages = QueueWorker()
                mensaje_enviado = queue_messages.queue_busqueda(busquedaId + "$query=" + query)
                if mensaje_enviado:
                    logging.info(f'Busqueda enviada a FoodApi')
                    return busquedaId, 202
                else:
                    logging.info(f'Error al enviar mensaje en el queue')
                    return "Error en el servidor", 500
    except Exception as exc:
        logging.error(f'ERROR: No se pudo registrar busqueda: {exc}')
        return None, 500


@app.route("/busqueda", methods=['POST'])
def registrarBusqueda():
    try:
        #busqueda = Busqueda(producto)
        # busquedasCollection.insert(
        #     {
        #         'producto': busqueda.producto,
        #         'fecha': busqueda.fecha,
        #         'puntos': busqueda.puntos,
        #     }
        # )
        # return 'busqueda registrada'
        #print (request.get_json())
        return 'Busqueda recibida', 200
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
    numero_orden = request_json.get('OrderId')
    estado = request_json.get('OrderStatus')
    precio = request_json.get('TotalPrice')
    productos = request_json.get('Products')
    lst_productos = []
    for producto in productos:
        ingredientes = producto['Ingredients']
        lst_ingredientes = []
        for ingrediente in ingredientes:
            i = Ingrediente(
                nombre_ingrediente=ingrediente['Name'],
                cantidad_ingrediente=ingrediente['Amount'],
                unidad_ingrediente=ingrediente['Unit']
            )
            ingrediente_json = json.dumps(i, default=i.ingredienteADiccionario)
            lst_ingredientes.append(ingrediente_json)

        ing_objects = [json.loads(ing) for ing in lst_ingredientes]
        p = Producto(
            producto['Name'],
            producto['Servings'],
            producto['PricePerServing'],
            producto['Image'],
            ing_objects
        )
        producto_json = json.dumps(p, default=p.productoADiccionario)
        lst_productos.append(producto_json)

    orden = Orden(
        numero_orden,
        estado,
        precio,
        lst_productos
    )
    prod_objects = [json.loads(prod) for prod in orden.productos]
    ordenesCollection.insert_one(
        {
            'OrderId': orden.numero_orden,
            'Date': orden.fecha,
            'OrderStatus': orden.estado,
            'TotalPrice': orden.precio,
            'Products': prod_objects
        }
    )
    return 'orden generada'


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


@app.route("/ordenes/<OrderStatus>", methods=['GET'])
def listaOrdenesPorEstado(OrderStatus):
    try:
        logging.info(f'INICIO ==> OBTENER TODAS LAS ORDENES POR ESTADO')

        ordenes = [orden for orden in ordenesCollection.find({"OrderStatus": OrderStatus})]
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
        id = request_json.get("_id").get("$oid")
        estado = request_json.get("OrderStatus")
        query = {"_id": ObjectId(id)}
        update = { "$set": {"OrderStatus": estado}}
        ordenesCollection.update_one(query, update)
        return 'Orden actualizada'
    except Exception as exc:
        logging.error(f'ERROR: No se pudo actualizar orden: {exc}')
        return 'Orden NO actualizada'


# APP.RUN y puerto
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

