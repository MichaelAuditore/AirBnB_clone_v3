#!/usr/bin/python3
""" Reviews template """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage, place, amenity
from os import environ


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_by_place(place_id):
    """ Return all amenities linked to a place """

    s_place = storage.get(place.Place, place_id)
    if s_place is None:
        abort(404)

    if (environ.get('HBNB_TYPE_STORAGE') == 'db'):
        amenities = [a.to_dict() for a in s_place.amenities]
    else:
        amenities = [storage.get(amenity.Amenity, a).to_dict()
                     for a in s_place.amenity_ids]
    return (jsonify(amenities), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_place(place_id, amenity_id):
    """ Delete an amenity with the given ID and
    ID of a Place Object"""

    s_place = storage.get(place.Place, place_id)
    if not s_place:
        abort(404)

    s_amenity = storage.get(amenity.Amenity, amenity_id)
    if not s_amenity:
        abort(404)

    if (environ.get('HBNB_TYPE_STORAGE') == 'db'):
        if s_amenity not in s_place.amenities:
            abort(404)
        s_place.amenities.remove(amenity_id)
    else:
        if amenity_id not in s_place.amenity_ids:
            abort(404)
        s_place.amenity_ids.remove(amenity_id)
    storage.save()
    return (jsonify({}), 200)


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 methods=['POST'], strict_slashes=False)
def post_amenity_place(place_id, amenity_id):
    """ Add a new amenity based in place_id """

    s_place = storage.get(place.Place, place_id)
    s_amenity = storage.get(amenity.Amenity, amenity_id)

    if not s_place:
        abort(404)

    if not s_amenity:
        abort(404)

    if (environ.get('HBNB_TYPE_STORAGE') == 'db'):
        if s_amenity in s_place.amenities:
            return (jsonify(s_amenity.to_dict()), 200)
        else:
            place.amenities.append(s_amenity)
    else:
        if amenity_id in s_place.amenity_ids:
            return (jsonify(s_amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return (jsonify(s_amenity.to_dict()), 200)
