from flask import Flask, render_template, request, jsonify, render_template, url_for
import json
import requests

app = Flask(__name__)

loinc_map = {
    "89578-9": "FIRST_TRP",
    "8867-4": "HEART_RATE_MAX",
    "3094-0": "BUN",
    "26478-8": "lymph_leu_non_variant",
    "48643-1": "glome_M.p",
    "8462-4": "DIASTOLIC_BLOOD_PRESSURE_MAX",
    "29463-7": "BODY_WEIGHT_MIN",
    "30180-4": "Basophils.val",
    "26449-9": "EoS",
    "26499-4": "Neu/PMN/polys",
    "42637-9": "BnP",
    "30385-9": "RDW.val",
}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    input_dict = load_json_template()
    input_dict['ModelReq']['Age'] = int(request.form.get('Age'))
    input_dict['ModelReq']['Gender'] = request.form.get('Gender')

    for idx in range(len(input_dict['ModelReq']['Data'])):
        code = input_dict['ModelReq']['Data'][idx]['Code']
        value = float(request.form.get(loinc_map.get(code)))
        input_dict['ModelReq']['Data'][idx]['Results'][0]['result_value'] = value

    url = 'http://b19b12df-2d14-4820-accc-f58499f35b05.eastus2.azurecontainer.io/score'
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data=str.encode(json.dumps(input_dict)), headers=headers)
    output_dict = json.loads(r.json())
    return render_template('index.html',
                           prediction_text='Probability: {0}'.format(output_dict['ModelRes']['Data'][0]['Value']))


def load_json_template():
    json_file = 'input_template.json'
    input_dict = json.load(open(json_file))
    return input_dict
