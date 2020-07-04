from api.v1.get_resource import getMunicipios, getResourceId, getResourceFields
import os

def list_str(l_m):
	"""
	l_m lista de municipios para convertir en string
	"""
	string = ''
	for mun in l_m:
		string += mun[0]
		string += ','
	return string

def str_list(string):
	"""
	reverse the string to a list
	"""
	lista = string.split(',')[:-1]
	municipios = []
	for mun in lista:
		val1 = mun.split(':')[0]
		val2 = mun.split(':')[1]
		municipios.append((val1, val2))
	return municipios


def check_municipio(resource):
	file_name = 'Service/data/municipios/' + resource + '.txt'
	if os.path.exists(file_name):
		#print("leyendo de archivos")
		with open(file_name, 'r') as muns:
			municipios = muns.read()
			municipios = str_list(municipios)
			return municipios
	else:
		#print("scraping resource page")
		municipios = getMunicipios(getResourceId(resource)[1])
		mun_str = list_str(municipios)
		with open(file_name, 'w') as muns:
			muns.write(mun_str)
		return municipios

def check_condiciones(resource):
	file_name = 'Service/data/condiciones/' + resource + '.txt'
	if os.path.exists(file_name):
		#print("leyendo de archivos")
		with open(file_name, 'r') as muns:
			condiciones = muns.read()
			condiciones = str_list(condiciones)
			return condiciones
	else:
		#print("scraping resource page")
		condiciones = getResourceFields(getResourceId(resource)[1])
		cond_str = list_str(condiciones)
		with open(file_name, 'w') as conds:
			conds.write(cond_str)
		return condiciones