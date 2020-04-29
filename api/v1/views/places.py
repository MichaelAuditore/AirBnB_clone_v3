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


@app_views.route('v1/places_search', method=['POST'])
def places_by_objects():
    """Get all place Objects depending JSON body of the request"""

    content = request.get_json()

    if not content.is_json:
        abort(404, "Not a JSON")

        states = content['states']
        cities = content['cities']
        amenities = content['amenities']

    if (not states and not cities and not amenities):
        places = storage.all(place.Place).values()
        list_places = [p.to_dict() for p in places]
        return (jsonify(list_places))

    list_places = []
    if content.get('states'):
        obj = [storage.get(state.State, state_id)
               for state_id in content.get('states')]
        for st in obj:
            if st:
                for ct in st.cities:
                    if ct:
                        for pl in ct.places:
                            list_places.append(pl)

    if content.get('cities'):
        obj = [storage.get(city.City, city_id)
               for city_id in content.get('cities')]
        for ct in obj:
            if ct:
                for pl in ct.places:
                    if pl not in list_places:
                        list_places.append(pl)

    if content.get('amenities'):
        if not list_places:
            list_places = storage.all(place.Place).values()
        obj = [storage.get(amenity.Amenity, a)
               for a in content.get('amenities')]
        all_places = []
        for p in list_places:
            for a in obj:
                if (a in p.amenities):
                    all_places.append(a)

    final_list = []
    for p in all_places:
        d = p.to_dict()
        d.pop('amenities', None)
        final_list.append(d)

    return (jsonify(final_list))
