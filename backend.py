from flask import Flask
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
       # conference = python_fun(emailText)
       # resp = jsonify(conference), 201
        resp = 'Conference Extracted', 200
        return resp