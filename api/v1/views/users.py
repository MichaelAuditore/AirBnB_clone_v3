#!/usr/bin/python3
""" Users template """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage, user


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_users(user_id=None):
    """ If no id return all users, otherwise return matched user """
    if not user_id:
        all_users = storage.all(user.User).values()
        list_users = []
        for one_user in all_users:
            list_users.append(one_user.to_dict())
        return (jsonify(list_users))
    else:
        one_user = storage.get(user.User, user_id)
        if not one_user:
            abort(404)
        return (jsonify(one_user.to_dict()))


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Delete user based in given user_id """
    del_user = storage.get(user.User, user_id)
    if del_user is None:
        abort(404)
    storage.delete(del_user)
    storage.save()
    return (jsonify({}))


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """ Post a new user """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if 'email' not in content:
        abort(400, 'Migssing email')
    if 'password' not in content:
        abort(400, 'Missing password')
    new_user = user.User()
    new_user.email = content['email']
    new_user.password = content['password']
    if 'first_name' in content:
        new_user.first_name = content['first_name']
    if 'last_name' in content:
        new_user.last_name = content['last_name']
    storage.new(new_user)
    storage.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """ Put user based in id """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    one_user = storage.get(user.User, user_id)
    if one_user is None:
        abort(404)
    if 'first_name' in content:
        setattr(one_user, 'first_name', content['first_name'])
    if 'last_name' in content:
        setattr(one_user, 'last_name', content['last_name'])
    if 'password' in content:
        setattr(one_user, 'password', content['password'])
    storage.save()
    return(jsonify(one_user.to_dict()), 200)
