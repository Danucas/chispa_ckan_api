import requests, re
"""
Get Resource Data for the given recurso
"""


def getResourceId(res_name):
    """
    Get the resource ID to identify in the db
    return a list of ids
    the first for the last years record
    the second one for this year
    """
    if len(res_name) > 0:
        url = "https://cali.ckan.io/dataset/" + res_name
        response = requests.get(url)
        comp = 'href="/dataset/'+res_name+'/resource/'
        indexes = [m.start() for m in re.finditer(comp, response.text)]
        ids = []
        for title in indexes:
            start = title + len(comp)
            _id = ""
            while True:
                char = response.text[start]
                if char != '"':
                    _id += char
                    start += 1
                else:
                    if _id not in ids:
                        ids.append(_id)
                    break
        return (ids)
    return ([])


def getResourceFields(_id):
    """
    Get the table colum names
    """
    url = "https://cali.ckan.io/api/3/action/datastore_search"
    pars = {'resource_id': _id, 'q': 'fields'}
    res = requests.get(url, params=pars)
    fields = []
    for field in res.json()['result']['fields']:
        if 'info' in field and 'type' in field:
            fields.append({'label': field['info']['label'], 'type': field['type']})
    return (fields)

def getMunicipios(_id):
    """
    Get available municipalities, by the resource id
    """
    url = "https://cali.ckan.io/api/3/action/datastore_search"
    pars = {'resource_id': _id, 'q': ''}
    res = requests.get(url, params=pars)
    municipios = []
    for rec in res.json()['result']['records']:
        if 'MUNICIPIO' in rec:
            if not rec['MUNICIPIO'] in municipios:
                municipios.append(rec['MUNICIPIO'])
    choices = [('', '-----------')]
    for mun in municipios:
        choices.append((mun, mun.lower()))
    return (choices)

def getTest():
    """
    Tests the module
    """
    _id = getResourceId('hurto-a-residencias')
    return (getMunicipios(_id), getResourceFields(_id))
