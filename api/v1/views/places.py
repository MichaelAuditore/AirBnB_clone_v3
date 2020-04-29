#!/usr/bin/python3
""" Places template """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage, city, place, user


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Return all places linked to a city """
    s_city = storage.get(city.City, city_id)
    if s_city is None:
        abort(404)
    places = [p.to_dict() for p in s_city.places]
    return (jsonify(places), 200)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ Return a place that matches with the given ID """
    places = storage.get(place.Place, place_id)
    if places:
        return (jsonify(places.to_dict()), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Delete a city with the given ID """
    d_place = storage.get(place.Place, place_id)
    if d_place:
        storage.delete(d_place)
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Add a new place based in city_id """

    s_city = storage.get(city.City, city_id)
    content = request.get_json()

    if not s_city:
        abort(404)

    if not content:
        abort(400, "Not a JSON")

    if 'user_id' not in content:
        abort(400, "Missing user_id")

    if 'name' not in content:
        abort(400, "Missing name")

    s_user = storage.get(user.User, data['user_id'])

    if not s_user:
        abort(404)

    new_place = place.Place(**content)
    new_place.city_id = city_id
    new_place.save()
    return(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """ Update information in a place if ID exists """
    one_place = storage.get(place.Place, place_id)
    if one_place is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')

    ignore = ['id', 'created_at', 'updated_at', 'city_id', 'user_id']

    for key, val in content.items():
        if key not in ignore:
            setattr(one_place, key, value)
    storage.save()
    return(jsonify(one_place.to_dict()), 200)
