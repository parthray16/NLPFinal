from flask import Flask, json
from flask import request
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)

#CORS stands for Cross Origin Requests.
CORS(app) #Here we'll allow requests coming from any domain. Not recommended for production environment.

@app.before_first_request
def fill_calendar():
   # fillup calendar
    pass

@app.route('/', methods=['POST'])
def extract_conference():
    if request.method == 'POST':
        emailText = request.get_json()['text']
        extraction = { 'name': '', 'acronym': '', 'submission': '', 'notification': '', 'conference': '', 'location': '' }
        #extraction['name'] = pythonfunction(emailText)
        #extraction['acronym'] = pythonfunction(emailText)
        #extraction['submission'] = pythonfunction(emailText)
        #extraction['notification'] = pythonfunction(emailText)
        #extraction['conference'] = pythonfunction(emailText)
        #extraction['location'] = pythonfunction(emailText)
        #resp = jsonify(extraction), 200
        resp = jsonify({ 'name': '7th International Conference on Signal Processing and Integrated Networks', 'acronym': '', 'submission': '11/11/2019', 'notification': '12/9/2019', 'conference': '2/27/2020 - 3/1/2020', 'location': 'Delhi/NCR, India' }), 200
        return resp