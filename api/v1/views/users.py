#!/usr/bin/python3
'''users view'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    '''Return all the states in the storage'''
    state_object = storage.all(User)
    return jsonify([object.to_dict() for object in state_object.values()])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def search_user_by_id(user_id):
    '''Filter state by id'''
    object = storage.get(User, user_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    '''Delete state of the provided id'''
    object = storage.get(User, user_id)
    if object is None:
        abort(404)
    else:
        storage.delete(object)
        storage.save()
        # Return an empty dictionary with status code 200
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''Create a new state'''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()
        # if data is in json format, it return python dict or list
        # If the data is not valid JSON, raise an error or return None
        if 'email' not in data:
            abort(400, 'Missing email')
        if 'password' not in data:
            abort(400, 'Missing password')
        new_user = User(**data)
        # Create a new instance of state and pass the key value pairs
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201
    else:
        abort(400, 'Not a JSON')


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    '''Update state of provided id'''
    object = storage.get(User, user_id)
    if object is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    else:
        for key, value in data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(object, key, value)
        storage.save()
        return jsonify(object.to_dict()), 200
