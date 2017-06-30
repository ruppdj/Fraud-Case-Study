from build_model import FraudModel
from DataCleaner import DataCleaner
from save_to_db import dump_to_db, connect_to_db, disconnect_from_db, update_hash_db, get_hash_set_from_db
from urllib2 import Request, urlopen, URLError
import pandas as pd
import numpy as np
import json
import pickle
import hashlib
import time
import os
from datetime import datetime

def update_data(already_seen_set, db, model):

    url = "http://galvanize-case-study-on-fraud.herokuapp.com/data_point"
    req = Request(url)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
    else:
        # everything is fine
        data = response.read()

        # print type(data)

        hash_object = hashlib.md5(data)

        hash_value = hash_object.hexdigest()

        if hash_value not in already_seen_set:

            col_order = ['acct_type', 'approx_payout_date', 'body_length', 'channels',
                         'country', 'currency', 'delivery_method', 'description',
                         'email_domain', 'event_created', 'event_end', 'event_published',
                         'event_start', 'fb_published', 'gts', 'has_analytics',
                         'has_header', 'has_logo', 'listed', 'name', 'name_length',
                         'num_order', 'num_payouts', 'object_id', 'org_desc',
                         'org_facebook', 'org_name', 'org_twitter', 'payee_name',
                         'payout_type', 'previous_payouts', 'sale_duration',
                         'sale_duration2', 'show_map', 'ticket_types', 'user_age',
                         'user_created', 'user_type', 'venue_address', 'venue_country',
                         'venue_latitude', 'venue_longitude', 'venue_name', 'venue_state']

            input_dict = json.loads(data)

            df = pd.DataFrame([input_dict], columns=col_order)

            translation = ['not_fraud','maybe','fraud', 'top_prediction']

            prediction_list = model.predict_proba(df)[0]
           # prediction_list = np.array([.2,.3,.5])

            prediction_list = list(prediction_list) + [np.argmax(prediction_list)]

            prediction_dict = {translation[k]:v for k,v in enumerate(prediction_list)}

            timestamp_dict = {"time_stamp":datetime.now()}
            dump_to_db(db, input_dict, prediction_dict, timestamp_dict)

            update_hash_db(db, hash_value)

            already_seen_set.add(hash_value)

            print "..Data Retreived at: {}".format(str(datetime.now()))

    #sleep for 1 second before trying to retrieve data again
    time.sleep(1)
    return

def get_model():
    model = pickle.load(open("model.pkl", "rb"))
    return model

def run_all():

    #connect to db
    client, db = connect_to_db()

    #pull hash list of seen events from endpoint
    hash_set = get_hash_set_from_db(db)

    #load in model
    model = get_model()

    # update db every 1 second
    while True:
        update_data(hash_set, db, model)

    #disconnect from db
    disconnect_from_db(client)

if __name__ == "__main__":
    os.system('python app.py &')
    run_all()
