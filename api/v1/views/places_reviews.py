#!/usr/bin/python3
""" Cities template """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage, place, review, user


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Return all reviews linked to a place """
    s_place = storage.get(place.Place, place_id)
    if s_place is None:
        abort(404)
    print(s_place)
    cities = [c.to_dict() for c in s_place.reviews]
    return (jsonify(cities), 200)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Return a review that matches with the given ID """
    reviews = storage.all(review.Review).values()
    list_reviews = [c.to_dict() for c in reviews]
    for one_review in list_reviews:
        if one_review['id'] == review_id:
            return (jsonify(one_review))
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete a review with the given ID """
    reviews = storage.all(review.Review).values()
    for one_review in reviews:
        if one_review.id == review_id:
            storage.delete(one_review)
            storage.save()
            return(jsonify({}))
    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ Add a new review based in place_id """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in content:
        abort(400, 'Missing user_id')
    if 'text' not in content:
        abort(400, 'Missing text')
    one_state = storage.get(state.State, state_id)
    if one_state is None:
        abort(404)
    one_user = storage.get(user.User, content['user_id'])
    if one_user is None:
        abort(404)
    new_review = review.Review()
    new_city.text = content['text']
    new_city.user_id = content['user_id']
    new_city.place_id = place_id
    storage.new(new_review)
    storage.save()
    return(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """ Update information in a review if ID exists """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    one_review = storage.get(review.Review, review_id)
    if one_review is None:
        abort(404)
    setattr(one_review, 'text', content['text'])
    storage.save()
    return(jsonify(one_review.to_dict()), 200)
