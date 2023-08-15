from pymongo import MongoClient

client = MongoClient("mongodb+srv://qoabainc:ZvjX4J2edjU8woYW@cluster0.u2orl1m.mongodb.net/?retryWrites=true&w=majority")

db = client.test

collection_name = db["questions_app"]