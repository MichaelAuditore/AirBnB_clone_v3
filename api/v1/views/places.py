#!/usr/bin/python3
""" Places template """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage, city, place, user, amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Return all places linked to a city """
    s_city = storage.get(city.City, city_id)
    if not s_city:
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

    s_user = storage.get(user.User, content['user_id'])

    if not s_user:
        abort(404)

    if 'name' not in content:
        abort(400, "Missing name")

    content['city_id'] = city_id
    new_place = place.Place(**content)
    new_place.save()
    return(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """ Update information in a place if ID exists """
    one_place = storage.get(place.Place, place_id)

    if not one_place:
        abort(404)

    content = request.get_json()

    if not content:
        abort(400, 'Not a JSON')

    ignore = ['id', 'created_at', 'updated_at', 'city_id', 'user_id']

    for key, val in content.items():
        if key not in ignore:
            setattr(one_place, key, val)
    storage.save()
    return(jsonify(one_place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'])
def search_places():
    """return a list of places per state, city or amenity id
    do filters for each key into JSON passed to check
    """
    # JSON request is Empty or doesn't JSON
    content = request.get_json()
    if content is None:
        return jsonify('Not a JSON'), 400
    # Check JSON to know if empty or not if it's empty return all objects
    result, places = [], []
    if len(content) == 0:
        places = storage.all("Place").values()
        for elem in places:
            result.append(elem.to_dict())
        return jsonify(result)

    flag = 0
    for key in content:
        if len(content[key]) > 0:
            flag = 1
            break
    if flag == 0:
        places = storage.all("Place").values()
        for elem in places:
            result.append(elem.to_dict())
        return jsonify(result)
    # Check each Key, to get objects by state
    if "states" in content.keys() and len(content["states"]) > 0:
        states = content["states"]
        for id in states:
            st = storage.get("State", id)
            if st:
                for city in st.cities:
                    for pl in city.places:
                        places.append(pl)
    # Check each Key, to get objects by city excluding objects already are into
    if "cities" in content.keys() and len(content["cities"]) > 0:
        cities = content["cities"]
        for id in cities:
            ct = storage.get("City", id)
            if ct:
                for pl in ct.places:
                    places.append(pl)

    # Generate a list of unique values
    places = list(set(places))

    # Check amenities key, do a filter to add into final Place's object List
    if "amenities" in content.keys() and len(content["amenities"]) > 0:
        ame = []
        for id in content["amenities"]:
            ame.append(storage.get("Amenity", id))
        places = [pl for pl in places if all([a in pl.amenities for a in ame])]

    # Remove duplicate amenities
    for elem in places:
        var = elem.to_dict()
        if "amenities" in var.keys():
            del var["amenities"]
        result.append(var)

    return jsonify(result)
