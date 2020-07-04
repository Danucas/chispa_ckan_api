#!/usr/bin/python3
"""
Request to cali_ckan API
functions:
compare_last_year_this_month: (rec, ids, mun)
compare_last_year_today: (rec, ids, mun)
get_last_update: (rec, ids, mun)
"""


import requests
from .models import Service
from .get_resource import getResourceId
import re
import calendar
import json
from datetime import datetime

def read_dated_cache(rec):
    """
    Reads the stored date
    @rec: the resource name
    Return: date in YYYY-MM-DD format, false if file doesn0t exists
    """
    try:
        with open("Service/data/last_update", "r") as file:
            resources = json.loads(file.read())
            if rec in resources:
                resp = resources[rec].split(" ") 
            else:
                return False
            return resp
    except Exception as e:
        print(e)
        return False

def save_cache_date(rec, date):
    """
    Save date in last update
    @rec: the resource name
    @date: the date to save
    Return: nothing
    """
    try:
        objects = {}
        with open("Service/data/last_update", "r") as file:
            objects = json.loads(file.read())
        objects[rec] = ' '.join(date)
        with open("Service/data/last_update", "w") as writer:
            writer.write(json.dumps(objects))
    except Exception as e:
        with open("Service/data/last_update", "w") as file:
            file.write(json.dumps({}))
        print(e)
        save_cache_date(rec, date)


def request_month(month, id, mun):
    """
    Request data for the given month to Dataset
    @month: month to request
    @id: resource id to ask
    @mun: to filter by municipio
    Return: list of records or [] empty list
    """
    months = ["", "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO"]
    months.extend(["JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"])
    mes = months[month - 1]
    url = "https://cali.ckan.io/api/3/action/datastore_search"
    params = {"q": mes, "limit": 3000}
    params["resource_id"] = id
    month_res = []
    try:
        resp = requests.get(url, params=params)
        month_r = resp.json()["result"]["records"]
        for mon in month_r:
            if mun in mon['MUNICIPIO']:
                month_res.append(mon)
                # print(mon["MUNICIPIO"], mes)
    except Exception as e:
        print(e)
    return month_res


def save_result(fname, res):
    """
    Save json
    @fname: the file name to save
    @res: the json object to save
    """
    with open(fname, "w") as file:
        file.write(json.dumps(res, indent=2))


def get_last_update(res, ids, mun):
    """
    Get the last update date from html
    It's called from months trigger
    if it detects a change, request both months data and reply a message
    @res: the resource name
    @ids: the id for both databases
    @mun: municipio to request
    Return: (difference, month=>int value)
    """
    url = "https://cali.ckan.io/dataset/{}/resource/{}".format(res, ids[1])
    resp = requests.get(url)    
    comp = "Data last updated"
    occurencies = [oc.start() for oc in re.finditer(comp, resp.text)]
    for occ in occurencies:
        html = resp.text[occ+len(comp)+14:occ+len(comp)+40].strip()[4:]
        month, day, year = html.replace("<", " ").replace(",", "").split(" ")[0:3]
        months = [name for name in calendar.month_name]
        last = read_dated_cache(res)
        if last is False:
            save_cache_date(res, [month, day, year])
            return False
        print("last updated:", last)
        month = months.index(month)
        year = int(year)
        day = int(day)
        last[0] = months.index(last[0])
        if month != last[0]:
            print("Dataset has changed")
            last_mont = request_month(last[0], ids[1], mun)
            this_mont = request_month(month, ids[1], mun)
            save_result("last.json", last_mont)
            save_result("this.json", this_mont)
            last_length = len(last_mont)
            this_length = len(this_mont)
            if last_length == 0:
                # last_length = 1
                return (0, last[0])
            this_percent = (this_length * 100) / last_length
            diff = 100 - this_percent
            if diff < 0:
                print("The cases of {} in {} has been increase a {} % compared to {}".format(res.replace("-", " "), months[month - 1],
                                                                                                            int(diff * -1),
                                                                                                            months[last[0] - 1]
                                                                                                            ))
                return (diff, last[0])
            else:
                print("The cases of {} in {} has been decrease a {} % compared to {}".format(res.replace("-", " "), months[month - 1],
                                                                                                            int(diff),
                                                                                                            months[last[0] - 1]
                                                                                                            ))
                return (diff, last[0])

def compare_last_year_this_month(rec, ids, mun):
    """
    Compare this month with the last year at the same month
    @rec: the resource name
    @ids: the  ids for both databases
    @mun: the city to request
    Return: (difference, closest_year)
    """
    months = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"]
    months.extend(["Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"])
    month = datetime.now().month
    year = datetime.now().year - 1
    # request the last updated month
    this = request_month(month, ids[1], mun)
    save_result("this_month.json", this)
    url = "https://cali.ckan.io/api/3/action/datastore_search"
    #while True:
    # if doesn't get any register try the year before
    params = {"q": months[month], "limit": 3000}
    params["resource_id"] = ids[0]
    resp = requests.get(url, params=params)
    last = resp.json()["result"]["records"]
    la = []
    while year > 2009:
        for l in last:
            # print("searching in", json.dumps(l, indent=2))
            if mun in l['municipio'] and l['anio'] == year:
                la.append(l)
        if len(la) < 1:
            year -= 1
        else:
            break
        print("retry: ", year)
    last = la
    # save_result("last_year.json", last)
    percent_this = (len(this) * 100) / len(last)
    print(len(this), len(last))
    diff = 100 - percent_this
    if diff < 0:
        print("{} increase in {} % from {}".format(rec.replace("-", " "), int(diff * -1), year))
        return (diff, year)
    else:
        print("{} decrease in {} % from {}".format(rec.replace("-", " "), int(diff), year))
        return (diff, year)


def compare_last_year_today(rec, ids, mun):
    """
    Compare today with the last year at this same day
    @rec: the resource name to request
    @ids: Both databases ids
    @mun: the city to request
    Return: (cases_count, date_string)
    """
    date_t = datetime.now()
    year = date_t.year - 1
    count = 0
    query = {"q": "{}".format(mun), "limit": 3000}
    query["resource_id"] = ids[0]
    url = 'https://cali.ckan.io/api/3/action/datastore_search'
    resp = requests.get(url, params=query)
    records = resp.json()["result"]["records"]
    while count < 1:
        date = '-'.join([str(year), '{:0>2}'.format(date_t.month), '{:0>2}'.format(date_t.day)])
        for re in records:
            if re['fecha'] == date:
                count += 1
        if count == 0:
            year -= 1
    print("El {} hubo {} casos de {}".format(date, count, rec))
    with open("test", "w") as file:
        file.write(json.dumps(resp.json(), indent=2))
    return count, date


# def get_reg_by_years(service_id):
#     """
#     Request register by year

#     """
#     service = Service.objects.get(id=service_id)
#     rec = service.recurso
#     mun = service.municipio
#     mun = 'CALI'
#     condiciones = {}
#     for cond in service.condicion.split(',')[:-1]:
#         condiciones[cond.split(':')[0]] = cond.split(':')[1]
#     print(rec, mun, condiciones)
    
#     ids = getResourceId(rec)
#     compare_last_year_this_month(rec, ids, mun)
