#!/usr/bin/python3
from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger, LazyJSONEncoder, LazyString
from api.v1.datasets import app_datasets
from api.v1.docs import template

app = Flask(__name__)
CORS(app)
app.register_blueprint(app_datasets)
app.config['SWAGGER'] = {
    'title': 'Chispa CKAN',
    'uiversion': 3
}
app.json_encoder = LazyJSONEncoder
swagger = Swagger(app, template=template)
@app.errorhandler(500)
def server_error(error):
    """
    Capture and print error
    """
    print(error)
    return jsonify(error='Server error', message=str(error)), 500


@app.errorhandler(404)
def not_found(error):
    """
    Catch not found errors
    """
    print(error)
    return jsonify(error=str(error)), 404


@app.route('/', strict_slashes=False)
def index():
    """
    Return a welcome to CKAN Chispa datasets
    """
    return 'Welcome to cali.ckan.io'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080')