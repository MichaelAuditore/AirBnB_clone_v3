#!/usr/bin/python3
"""Templates views"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models import amenity, city, place, review, state, user


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """Return a JSON string with status"""
    return (jsonify({"status": "OK"}))


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def count_objs():
    """ Count the number of objs by class """
    count_objs = {
        "amenities": storage.count(amenity.Amenity),
        "cities": storage.count(city.City),
        "places": storage.count(place.Place),
        "reviews": storage.count(review.Review),
        "states": storage.count(state.State),
        "users": storage.count(user.User)
    }
    return (jsonify(count_objs))
