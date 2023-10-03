#!/usr/bin/python3
'''amenities view'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    '''Return all the states in the storage'''
    state_object = storage.all(Amenity)
    return jsonify([object.to_dict() for object in state_object.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def search_amenity_by_id(amenity_id):
    '''Filter state by id'''
    object = storage.get(Amenity, amenity_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    '''Delete state of the provided id'''
    object = storage.get(Amenity, amenity_id)
    if object is None:
        abort(404)
    else:
        storage.delete(object)
        storage.save()
        # Return an empty dictionary with status code 200
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''Create a new state'''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()
        # if data is in json format, it return python dict or list
        # If the data is not valid JSON, raise an error or return None
        if 'name' not in data:
            abort(400, 'Missing name')
        new_amenity = Amenity(**data)
        # Create a new instance of state and pass the key value pairs
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201
    else:
        abort(400, 'Not a JSON')


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''Update state of provided id'''
    object = storage.get(Amenity, amenity_id)
    if object is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    else:
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(object, key, value)
        storage.save()
        return jsonify(object.to_dict()), 200
