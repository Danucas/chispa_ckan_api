#!/usr/bin/python3
"""
Import the routes to request the datasets
"""

from flask import Blueprint

app_datasets = Blueprint('api_datasets', __name__, url_prefix='/api/v1')

from api.v1.datasets.index import *