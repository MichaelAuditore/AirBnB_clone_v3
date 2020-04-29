#!/usr/bin/python3
""" Cities template """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage, city, state


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """ Return all cities linked to a state """
    cities = storage.all(city.City).values()
    filter_cities = []
    if state_id is not None:
        list_cities = [c.to_dict() for c in cities]
        for one_city in list_cities:
            if one_city['state_id'] == state_id:
                filter_cities.append(one_city)
    if len(filter_cities) != 0:
        return (jsonify(filter_cities))
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ Return a City that matches with the given ID """
    cities = storage.all(city.City).values()
    list_cities = [c.to_dict() for c in cities]
    for one_city in list_cities:
        if one_city['id'] == city_id:
            return (jsonify(one_city))
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Delete a city with the given ID """
    cities = storage.all(city.City).values()
    for one_city in cities:
        if one_city.id == city_id:
            storage.delete(one_city)
            storage.save()
            return(jsonify({}))
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ Add a new city based in state_id """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if 'name' not in content:
        abort(400, 'Missing name')
    one_state = storage.get(state.State, state_id)
    if one_state is None:
        abort(404)
    new_city = city.City()
    new_city.name = content['name']
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """ Update information in a city if ID exists """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    one_city = storage.get(city.City, city_id)
    if one_city is None:
        abort(404)
    setattr(one_city, 'name', content['name'])
    storage.save()
    return(jsonify(one_city.to_dict()), 200)
