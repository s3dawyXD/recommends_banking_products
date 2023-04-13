import os
import sys
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from machine_learning_module import recommendation_engine
from datetime import datetime
import pandas as pd 
from werkzeug.utils import secure_filename
app = Flask(__name__)

CORS(app)
ALLOWED_EXTENSIONS = {'csv'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-predict', methods=['POST'])
def file_predict():
    if not request.files:
        return abort(400)
    file = request.files['file']
    if file and allowed_file(file.filename):
        df = pd.read_csv(file)
        predictions = recommendation_engine.predict(df)
        return jsonify({
                'success': True,
                "expected_products":predictions
            }), 200



@app.route('/single-predict', methods=['POST'])
def single_predict():
    try:
        body = request.get_json()
        data = {
            "fecha_dato": [datetime.today().strftime('%Y-%m-%d')],
            "ncodpers": [body.get("ncodpers")], 
            "ind_empleado": [body.get("ind_empleado")],
            "pais_residencia": [body.get("pais_residencia")],
            "sexo": [body.get("sexo")],
            "age": [body.get("age")],
            "fecha_alta": [body.get("fecha_alta")],
            "ind_nuevo": [body.get("ind_nuevo")],
            "antiguedad": [body.get("antiguedad")],
            "indrel": [body.get("indrel")],
            "ult_fec_cli_1t": [body.get("ult_fec_cli_1t")],
            "indrel_1mes": [body.get("indrel_1mes")],
            "tiprel_1mes": [body.get("tiprel_1mes")],
            "indresi": [body.get("indresi")],
            "indext": [body.get("indext")],
            "conyuemp": [body.get("conyuemp")],
            "canal_entrada": [body.get("canal_entrada")],
            "indfall": [body.get("indfall")],
            "tipodom": [body.get("tipodom")],
            "cod_prov": [body.get("cod_prov")],
            "nomprov": [body.get("nomprov")],
            "ind_actividad_cliente": [body.get("ind_actividad_cliente")],
            "renta": [body.get("renta")],
            "segmento": [body.get("segmento")],
        }
        df = pd.DataFrame.from_dict(data)
        predictions = recommendation_engine.predict(df)
        return jsonify({
                'success': True,
                "expected_products":predictions
            }), 200
    except:
        abort(400)


'''
error handlers
'''

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    print("Unexpected error:", sys.exc_info()[0])
    return jsonify({
        'success': False,
        "error": 400,
        "message": "Bad Request"
    }), 400


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        "error": 422,
        "message": "Unprocessable Request"
    }), 422


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        "error": 401,
        "message": "Unauthorized Request"
    }), 401