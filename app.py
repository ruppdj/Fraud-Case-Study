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

@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello World!'

@app.route('/score', methods = ['GET','POST'])
def score():
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
    return render_template('score.html',  nf= nf,len_nf=len(nf),\
    mb = mb, len_mb=len(mb), fr = fr, len_fr=len(fr))

@app.route('/feedback', methods = ['GET','POST'])
def feedback():
    switch = int(request.form.get('switch'))
    orgname = str(request.form.get('orgname'))
    inputdata = int(request.form.get('id'))
    if switch == 1:
        mongo_client = MongoClient()
        db = mongo_client.p1_database
        coll = db.web_input
        coll.remove({"object_id":(inputdata)})
        no_change = 1
    else:
        no_change = 0
    return render_template('feedback.html', nc = no_change, id= inputdata, orgname= orgname)


if __name__ == '__main__':
    mongo_client = MongoClient()
    app.run(host='0.0.0.0', port=5000, debug=True)
