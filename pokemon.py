import requests

api_base_url = "https://pokeapi.co/api/v2/"  # url base de la api
limit_registers = 100  # la api por defecto solo retorna 20 registros, por lo cual con esta variable podemos cambiar eso (si quisieramos traer más de 20 registros a la vez)


def pokemons_with_at():
	"""
	función que entrega la cantidad de pokemones que tienen la cadena 'at' y dos letras 'a' en su nombre.

	returns: int -> numero de pokemones cuyo nombre contiene al menos una vez la cadena 'at' y exactamente dos veces la letra 'a'
	"""

	target_endpoint = api_base_url + "pokemon/?limit=" + str(limit_registers)
	next_query = target_endpoint  # variable que contiene la siguiente consulta a realizar
	found_pokemons = 0  # se inicializa la variable que contendrá el resultado final
	while next_query:  # mientras haya más registros que consultar
		api_request = requests.get(next_query)  # se realiza la request a la api
		json_response = api_request.json()  # se obtiene la respuesta json, se podría implementar algún tipo de manejo de errores (ej: 500), pero para el problema asumiremos que la api funciona :D
		for pokemon in json_response['results']:  # se recorren los registros (pokemones) obtenidos
			pokemon_name = pokemon['name']  # se extrae el nombre del pokemon (no es tan necesario, pero a mi juicio hace más limpio el código)
			if 'at' in pokemon_name and pokemon_name.count('a') == 2:  # tal vez esto se podría optimizar cosa de recorrer 1 sola vez el string, pero el código podría quedar super enrredado D:
				found_pokemons += 1  # encontramos un pokemon que cumple con las características :D
		next_query = json_response['next']  # vemos si quedan más registros por consultar
	return found_pokemons  # se retorna el resultado que encontramos :)


def raichu_partners():
	"""
	función que entrega la cantidad de especies con las cuales raichu puede procrear.

	returns: int -> número de especies con las cuales raichu puede procrear
	"""

	species_endpoint = api_base_url + "pokemon-species/raichu/"  # con este endpoint podemos saber a que 'egg groups' está asociado raichu
	api_request = requests.get(species_endpoint)
	species_json_response = api_request.json()
	raichu_egg_groups = []  # variable que almacenará los 'egg groups' a los que pertenece raichu
	raichu_partners = dict()  # inicializamos este diccionario que contendrá todos los compañeros de 'egg group' de raichu. Se inicializa como un diccionario ya que así podemos ver si un elemento ya está en el dict (para evitar duplicados) en tiempo O(1), a diferencia de una lista la cual habría que recorrer a mano buscando el elemento
	for egg_group in species_json_response['egg_groups']:  # en este loop extraemos solamente el nombre de los 'egg groups' a los que está asociado raichu
		raichu_egg_groups.append(egg_group['name'])
	egg_group_endpoint = api_base_url + "egg-group/"  # endpoint que contiene el detalle de cada 'egg group'
	for egg_group in raichu_egg_groups:  # para cada egg group de raichu, consultamos su detalle
		egg_group_query = egg_group_endpoint + egg_group
		api_request = requests.get(egg_group_query)
		egg_json_response = api_request.json()
		group_pokemons = egg_json_response['pokemon_species']  # extraemos las especies de pokemones que están en cada 'egg group'
		for pokemon in group_pokemons:
			raichu_partners[pokemon['name']] = True  # la gracia de esto es que evita los duplicados, ya que si el pokemon ya estaba en el diccionario, únicamente sobrescribirá su valor (y no añadirá un nuevo registro).
	return len(raichu_partners.keys())  # finalmente, el total de especies con las que puede procrear raichu es el largo de las llaves del diccionario


def fighting_weight():
	"""
	función que entrega el peso máximo y el peso mínimo de los pokemones de tipo lucha de primera generación

	returns: list[int] -> lista que contiene el peso máximo y mínimo de los pokemones tipo lucha de primera generación
	"""

	types_endpoint =  api_base_url + "type/fighting/"  # endpoint del cual se extraen todos los pokemones asociados al tipo luchador
	types_api_request = requests.get(types_endpoint)
	json_response = types_api_request.json()
	fighting_pokemons = json_response['pokemon']  # extraemos la lista de pokemones que están asociados al tipo lucha
	max_weight = -1  # inicializamos el máximo en -1 (cualquier peso de un pokemon será superior a este valor)
	min_weight = float('inf')  # inicializamos el mínimo en infinito (cualquier peso de un pokemon será inferior a este valor)
	for pokemon in fighting_pokemons:  # recorremos los pokemones luchadores
		pokemon_url = pokemon['pokemon']['url']  # cada registro retornado por la api no tiene directamente el id del pokemon, pero si tiene una url de la forma 'https://pokeapi.co/api/v2/pokemon/ID/', de la cual podemos extraer el id sin la necesidad de consultar nuevamente la api
		pokemon_id = int(pokemon_url.split('/')[-2])  # extraemos la id del pokemon desde la url
		if pokemon_id <= 151:  # para tomar solo los pokemones de primera generación (cuyo id sea inferior o igual a 151)
			pokemon_endpoint = api_base_url + "pokemon/" + str(pokemon_id)  # formamos la url target para consultar por el detalle del pokemon
			pokemon_api_request = requests.get(pokemon_endpoint)
			json_response = pokemon_api_request.json()
			pokemon_weight = json_response['weight']  # extraemos el peso del pokemon
			max_weight = max(max_weight, pokemon_weight)  # comparamos el peso del pokemon con el peso máximo hasta ahora
			min_weight = min(min_weight, pokemon_weight)  # comparamos el peso del pokemon con el peso mínimo hasta ahora
	return [max_weight, min_weight]  # retornamos la lista con el peso [máx, min]
