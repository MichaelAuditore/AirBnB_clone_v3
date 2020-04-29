#!/usr/bin/python3
"""State Template"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def show(amenity_id=None):
    """return All amenity objects or a specific amenity object by id"""
    if not amenity_id:
        all_amenities = storage.all(Amenity).values()
        list_amenities = [amenity.to_dict() for amenity in all_amenities]
        return jsonify(list_amenities)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)

        return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """Deletes an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/amenities/", methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an Amenity"""
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    kwargs = request.get_json()
    amenity = Amenity(**kwargs)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates an Amenity object"""
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
        amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for key, val in content.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, val)
    storage.save()
    return jsonify(amenity.to_dict()), 200
