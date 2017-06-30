<h1>
Fraud Case Study


<h2>Objective:
<h6>
Our team of three people was given 2 days to create a model and user interface to detect possible fraud. The system pulls json files from a API and classifies them storing the result in a mongoDB.  A web user interface is then accessible for client review of activity.

<h2>Files:
<h6>
build_model.py : This is used to build a pickle the tested model for use.  It also contains the class FraudModel which incapsulates the functionality for the API's and Data Cleaning / preprocessing.

DataCleaner.py : A class that executes the required proposing for the data before being modeled.  Also cleans any new data before the model predicts the probability of fraud.

model.pkl : The stored model used in analysis of new data.

save_to_db.py: a helper file used to connect to the db and send/receive data

live.py: this launches the web server (app.py) then it runs a function that hits the endpoint every second continuously updating the database




<h2>Model: 
<h6>
We used a RandomForest model on 12 fields. The classifier has three possible outcomes. The Model was trained with the idea that the 'acct_tyep' field will translate to the below.

0 : Not Fraud - 'premium'
1 : Maybe Fraud - 'spammer_warn', 'spammer_limited', 'spammer_noinvite', 'locked', 'tos_lock', 'tos_warn', 'fraudster_att', 'spammer_web', 'spammer'
2 : Fraud - 'fraudster_event', 'fraudster'


<h2>Results:
<h6>
The current model has a cross validation score of 92%.


<h2>Conclusion:
<h6>
The following steps should still be taken:
1) Modifications to the Model.
  a) More analysis on the fields to find importance.
  b) Adding a TF-IDF classification on the Description field.
