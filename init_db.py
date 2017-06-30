import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.p1_database
coll = db.web_input
coll = db.hash_db
coll.insert({'hash_record':'1','hash_set':[]})

client.close()
