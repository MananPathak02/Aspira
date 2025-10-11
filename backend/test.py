from pymongo import MongoClient

client = MongoClient("CONNECTION_STRING")
db = client['aspiraDB']
print(db.list_collection_names())
