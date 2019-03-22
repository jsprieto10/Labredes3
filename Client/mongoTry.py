import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.redes

user = 'sebastian'
password = '1234'
u = db.usuarios.find_one({'user': user, 'password': password})

print(u if u else 'No encontrado')
