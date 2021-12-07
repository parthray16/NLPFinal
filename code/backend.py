from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from extractions import get_dates, get_location, get_name

app = Flask(__name__)

#CORS stands for Cross Origin Requests.
CORS(app) #Here we'll allow requests coming from any domain. Not recommended for production environment.


@app.route('/', methods=['POST'])
def extract_conference():
    if request.method == 'POST':
        emailText = request.get_json()['text']
        extraction = { 'name': '', 'submission': '', 'notification': '', 'conference': '', 'location': '' }
        extraction['name'] = get_name(emailText)
        dates = get_dates(emailText.lower())
        extraction['submission'] = dates[1] if dates[1] else '' 
        extraction['notification'] = dates[2] if dates[2] else ''
        extraction['conference'] = dates[0] if dates[0] else ''
        extraction['location'] = get_location(emailText)
        resp = jsonify(extraction), 200
        return resp