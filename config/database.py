from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://sadmorph:Suckduck228_@test.7fazc.mongodb.net/?retryWrites=true&w=majority&appName=Test"

client = MongoClient(uri, server_api=ServerApi("1"))  # Добавил ServerApi

db = client.todo_db

print("Доступные базы:", client.list_database_names())
print("Доступные коллекции:", db.list_collection_names())

collection = db["todo_collection"]
users_collection = db["users_collection"]
