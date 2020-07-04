import requests, re
import os
from api.v1.get_resource import getResourceId
from api.v1.serialize import str_list, list_str
"""
Get the recursos local data
"""


def get_datasets():
    """
    Get datasets from ckan
    """
    response = requests.get("https://cali.ckan.io/dataset")
    indexes = [m.start() for m in re.finditer("dataset-heading", response.text)]
    dsets = []
    for title in indexes:
        start = title + len('dataset-heading">')
        dt = ""
        while True:
            char = response.text[start]
            if char != '>':
                dt += char
                start += 1
            else:
                break
        ds = dt.split('"')[1].split('/')[2]
        dsets.append(ds)    
    dsets_str = list_str(dsets)
    return dsets
