from pymongo import MongoClient

client = MongoClient("mongodb+srv://<user>:<password>@cluster0.u2orl1m.mongodb.net/?retryWrites=true&w=majority")

db = client.test

collection_name = db["todos_app"]