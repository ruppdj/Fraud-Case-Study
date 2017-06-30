import pymongo
from pymongo import MongoClient
import json


def dump_to_db(db, inputs, prediction, timestamp):
    # inputs is a dictionary of the feature labels:values
    # prediction is a dictionary of predicitons {fraud:%, maybe:%, not:%}
    # combine these dictionaries,jsonify, then dump to db

    coll = db.web_input

    # combine dictionaries
    inputs.update(prediction)
    inputs.update(timestamp)

    # jsonify the dictionary
    #json_string = json.dumps(combined_dict)

    # save to database
    coll.insert(inputs)

    return

#
# ttt = {'a':120, 'b':'hello', 'c':'world'}
# tt = {'d':6}
# dump_to_db(ttt,tt)

def connect_to_db():
    # make db connection
    client = MongoClient()
    return client, client.p1_database

def disconnect_from_db(client):
    client.close()
    return

def update_hash_db(db, hash_string):
    db.hash_db.update_one({'hash_record':'1'},
                               {'$addToSet' : {'hash_set':hash_string}})

def get_hash_set_from_db(db):
    hash_dict = db.hash_db.find_one({'hash_record':'1'})

    #print json_doc

    #hash_list_dict = json.loads(json_doc)

    hash_set = set(hash_dict['hash_set'])

    return hash_set



