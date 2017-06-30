from flask import Flask, render_template, request
from pymongo import MongoClient
app = Flask(__name__)

# @app.route('/')
# def index():
#      return render_template('index.html')

# @app.route('/submitpage')
# def submit():
#     return render_template('submit.html')
#
@app.route('/works')
def api_works():
    return 'Everything does'

@app.route('/broken')
def api_broken():
    return 'Nothing is'

#testing
@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello World!'


@app.route('/score', methods = ['GET','POST'])
'''
the following codes will set up score page.
the score page will display
1. overall prediction results which contains
    a: total number of non-flaud events
    b: total number of possibly flaud events
    c: total number of highly flaud events

2. tables of non-flaud, possibly flaud and highly flaud events.
    each table contains
    a: Object_ID
    b: Organization Name
    c: Country of the event
    d: Prediction percentage of event being non-flaud event
    e: Prediction percentage of event being possibly flaud event
    f: Prediction percentage of event being highly Fraud event
    g: timestamp of the event
    h: radio button which asks users if users contacted the event Organization
        - if user select "yes" and press submit button, program will delete
        event and event information from database
        - if user select "no" and press submit button, event information
        including event id, organization name and their contact will be displayed
'''
def score():
    # access mongodb and store all non-flaud, possibly flaud and highly flaud
    # events into 3 different lists
    mongo_client = MongoClient()
    db = mongo_client.p1_database
    coll = db.web_input
    not_fraud = coll.find({"top_prediction":0})
    nf = []
    for i in not_fraud:
        nf.append(i)
    maybe = coll.find({"top_prediction":1})
    mb = []
    for i in maybe:
        mb.append(i)
    fraud = coll.find({"top_prediction":2})
    fr = []
    for i in fraud:
        fr.append(i)
    #return "this is not_fraud: {}".format(not_fraud)
    mongo_client.close()

    # returns lists and length of lists to score.html template.
    # information will be used to create tables
    return render_template('score.html',  nf= nf,len_nf=len(nf),\
    mb = mb, len_mb=len(mb), fr = fr, len_fr=len(fr))

@app.route('/feedback', methods = ['GET','POST'])
'''
the following codes will set up feedback page.
the feedback page will be displayed only when user select radio button and
click submit button in the score page.

the feedback page contains following:
1. If user selected "yes" radio button:
    - open mongodb and delete event with specific object id from the database.
    - display message "object id is removed from the database!"
2. If user selected "no" radio button:
    - open feedback page with table containing event id, event organization
    name and their e-mail address.
    - Since we do not have actual e-mail address, the page displays fake
    e-mail address (ilovemoney@gmail.com)
'''
def feedback():
    # gets information from score page
    switch = int(request.form.get('switch'))
    orgname = str(request.form.get('orgname'))
    inputdata = int(request.form.get('id'))
    if switch == 1:
        # if user selected "Yes", opens up mongodb and delete that
        #specific event from the database
        mongo_client = MongoClient()
        db = mongo_client.p1_database
        coll = db.web_input
        coll.remove({"object_id":(inputdata)})
        # the no_change will become a switch to initiate if statement in
        # our feedback page
        no_change = 1
    else:
        no_change = 0
    return render_template('feedback.html', nc = no_change, id= inputdata, orgname= orgname)


if __name__ == '__main__':
    mongo_client = MongoClient()
    app.run(host='0.0.0.0', port=5000, debug=True)
