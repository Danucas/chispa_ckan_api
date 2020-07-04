#!/usr/bin/python3
"""
This routes module performs a Scrapping to cali.ckan web page
and return a list of datasets and fields
"""

import json
from api.v1.datasets import app_datasets
from flask import jsonify, Response
from api.v1.get_datasets import get_datasets
from api.v1.get_resource import getResourceId, getResourceFields


@app_datasets.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returns ok status
    """
    return jsonify(status='OK'), 200


@app_datasets.route('/datasets', methods=['GET'], strict_slashes=False)
def datasets():
    """
    Datasets names and Ids
    Return a dictionary of datasets names
    containing the respective Ids for the past records and the 2020 records
    ---
    responses:
      200:
        description: a dictionary containing the names and ids for all datasets
        schema:
          type: object
          properties:
            homicidios:
              type: object
              properties:
                2020:
                  type: string
                  example: 53e3d2fe-0026-4bf0-ba69-687aa4904a0f
                past:
                  type: string
                  example: f465aa6b-a49f-42ce-8da2-fef524e7eada
    """
    datasets = get_datasets()
    dsets = {}
    for dset in datasets:
        print('getting', dset)
        res_ids = getResourceId(dset)
        dsets[dset] = {}
        dsets[dset]['2020'] = res_ids[1]
        dsets[dset]['past'] = res_ids[0]
    return Response(json.dumps(dsets), mimetype='application/json')


@app_datasets.route('/datasets/<dataset_id>', methods=['GET'], strict_slashes=False)
def datasets_info(dataset_id):
    """
    Dataset info by id
    Return a dictionary containing the fields for an specific dataset given by an Id
    ---
    parameters:
     - in: path
       name: dataset_id
       type: string
       required: true
       description: Id of the resource to fetch the info from
    responses:
      200:
        description: a dictionary containing the fields for the given id
        schema:
          type: object
          properties:
            f465aa6b-a49f-42ce-8da2-fef524e7eada:
              type: object
              properties:
                fields:
                  type: array
                  items:
                    type: object
                    properties:
                      label:
                        type: string
                        example: MES
                      type:
                        type: string
                        example: text
    """
    dset = {}
    dset[dataset_id] = {}
    dset[dataset_id]['fields'] = getResourceFields(dataset_id)
    return Response(json.dumps(dset), mimetype='application/json')


@app_datasets.route('/datasets/name/<dataset_name>', methods=['GET'], strict_slashes=False)
def datasets_info_by_name(dataset_name):
    """
    Dataset info by name
    Return a dictionary containing the fields for an specific dataset given by dataset name with no spaces
    joined by '-' character
    ---
    parameters:
     - in: path
       name: dataset_name
       type: string
       required: true
       description:  name with no spaces joined by the '-' character, example 'homicidios'
    responses:
      200:
        description: a dictionary containing the fields for each time range
        schema:
          type: object
          properties:
            homicidios:
              type: object
              properties:
                2020:
                  type: object
                  properties:
                    id:
                      type: string
                      example: b4fe8ba4-0d5b-4c8b-8c3b-85a20401ea3d
                    fields:
                      type: array
                      items:
                        type: object
                        properties:
                          label:
                            type: string
                            example: MES
                          type:
                            type: string
                            example: text
                past:
                  type: object
                  properties:
                    id:
                      type: string
                      example: b4fe8ba4-0d5b-4c8b-8c3b-85a20401ea3d
                    fields:
                      type: array
                      items:
                        type: object
                        properties:
                          label:
                            type: string
                            example: fecha
                          type:
                            type: string
                            example: timestamp
    """
    dsets = {}
    res_ids = getResourceId(dataset_name)
    dsets[dataset_name] = {}
    dsets[dataset_name]['2020'] = {}
    dsets[dataset_name]['past'] = {}
    dsets[dataset_name]['2020']['id'] = res_ids[1]
    dsets[dataset_name]['past']['id'] = res_ids[0]
    dsets[dataset_name]['2020']['fields'] = getResourceFields(res_ids[1])
    dsets[dataset_name]['past']['fields'] = getResourceFields(res_ids[0])
    return Response(json.dumps(dsets), mimetype='application/json')

@app_datasets.route('/datasets/complete', methods=['GET'], strict_slashes=False)
def datasets_complete_info():
    """
    Complete datasets
    Return a dictionary of datasets names containing the respective Ids for the past records and the 2020 records
    and each id containing the fields for the dataset and the value type for each one
    ---
    responses:
      200:
        description: a dictionary of datasets
        schema:
          type: object
          properties:
            homicidios:
              type: object
              properties:
                2020:
                  type: object
                  properties:
                    id:
                      type: string
                      example: b4fe8ba4-0d5b-4c8b-8c3b-85a20401ea3d
                    fields:
                      type: array
                      items:
                        type: object
                        properties:
                          label:
                            type: string
                            example: MES
                          type:
                            type: string
                            example: text
                past:
                  type: object
                  properties:
                    id:
                      type: string
                      example: b4fe8ba4-0d5b-4c8b-8c3b-85a20401ea3d
                    fields:
                      type: array
                      items:
                        type: object
                        properties:
                          label:
                            type: string
                            example: fecha
                          type:
                            type: string
                            example: timestamp
    """
    datasets = get_datasets()
    dsets = {}
    for dset in datasets:
        print('getting', dset)
        res_ids = getResourceId(dset)
        dsets[dset] = {}
        dsets[dset]['2020'] = {}
        dsets[dset]['past'] = {}
        dsets[dset]['2020']['id'] = res_ids[1]
        dsets[dset]['past']['id'] = res_ids[0]
        dsets[dset]['2020']['fields'] = getResourceFields(res_ids[1])
        dsets[dset]['past']['fields'] = getResourceFields(res_ids[0])
    return Response(json.dumps(dsets), mimetype='application/json')