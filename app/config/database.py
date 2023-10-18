from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Calculate path to .env file in the main directory
dotenv_path = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), '.env')

# Load environment variables from .env file
load_dotenv(dotenv_path)

mongo_username = os.environ.get("MONGO_USERNAME")
mongo_password = os.environ.get("MONGO_PASSWORD")

if not (mongo_username and mongo_password):
    raise ValueError(
        "MongoDB username and/or password not provided in environment variables.")

# Construct the connection string
mongo_connection_string = f"mongodb+srv://{mongo_username}:{mongo_password}@cluster0.u2orl1m.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(mongo_connection_string)

db = client.test

question_collection = db["questions_app"]
account_collection = db["accounts"]
user_collection = db["users"]
stats_collection = db["statistics"]
