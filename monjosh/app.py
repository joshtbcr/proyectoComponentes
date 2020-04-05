from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os

app = Flask(__name__)
title = "Monjosh App"
heading = "Monjosh App"

##Un-Comment when running against the Cosmos DB Emulator
client = MongoClient("mongodb://monjoshdb:2PBsBQi43gAKECaFF8A1bYrQeEHxVUrllDN82V8T3gcTrOsPFT6TqeHdqHyNXJbDoYOWorosspRW2pXrT8YVlQ==@monjoshdb.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@monjoshdb@") #host uri
db = client.monjoshdb
db.authenticate(name="monjoshdb",password='2PBsBQi43gAKECaFF8A1bYrQeEHxVUrllDN82V8T3gcTrOsPFT6TqeHdqHyNXJbDoYOWorosspRW2pXrT8YVlQ==')

collection = db.productos

@app.route('/')
def hello():
    return 'This Compose/Flask demo has been viewed'

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	productoid='1001'
	collection.insert({ "productoid":productoid, "name":"productoprueba"})
	return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5000)