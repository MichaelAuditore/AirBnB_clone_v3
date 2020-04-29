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
    if request.get_json() is not None:
        content = request.get_json()
        states = content.get('states', [])
        cities = content.get('cities', [])
        amenities = content.get('amenities', [])
        amenity_objects = []
        for amenity_id in amenities:
            amenity = storage.get('Amenity', amenity_id)
            if amenity:
                amenity_objects.append(amenity)
        if states == cities == []:
            places = storage.all('Place').values()
        else:
            places = []
            for state_id in states:
                state = storage.get('State', state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get('City', city_id)
                for place in city.places:
                    places.append(place)
        last_places = []
        for place in places:
            place_amenities = place.amenities
            last_places.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    last_places.pop()
                    break
        return jsonify(last_places)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
