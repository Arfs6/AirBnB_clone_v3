#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""All views for state model"""

from json import dumps
from flask import make_response, abort, request
from api.v1.views import app_views
import models


def _jsonify(data):
    """Converts @data into a json string,
    make a response with the string and set application/json header.
    """
    response = make_response(data)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/states')
def allStates():
    """Retrieves all states."""
    data = [
        obj.to_dict()
        for obj in models.storage.all(models.state.State).values()
    ]
    return _jsonify(data)


@app_views.route('/states/<state_id>')
def stateById(state_id):
    """Return the State object with id attribute = @state_id"""
    data = models.storage.get(models.state.State, state_id)
    if not data:
        return abort(404)
    return _jsonify(data.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def deleteState(state_id):
    """Delete State with id = @state_id"""
    data = models.storage.get(models.state.State, state_id)
    if not data:
        return abort(404)
    data.delete()
    models.storage.save()
    return _jsonify({})


@app_views.route('/states', methods=['POST'])
def createState():
    """Creates a State object."""
    requestDict = request.get_json(silent=True)
    if requestDict is None:
        abort(400, 'Not a JSON')
    elif not requestDict.get('name'):
        abort(400, 'Missing name')
    newState = models.state.State()
    newState.name = requestDict['name']
    newState.save()
    return _jsonify(newState.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def updateState(state_id):
    """Update attributes of a State object."""
    stateObj = models.storage.get(models.state.State, state_id)
    if not stateObj:
        abort(404)
    requestDict = request.get_json(silent=True)
    if requestDict is None:
        abort(400, 'Not a JSON')
    ignoreList = ['id', 'created_at', 'updated_at']
    for key, value in requestDict.items():
        if key in ignoreList:
            continue
        setattr(stateObj, key, value)
    stateObj.save()
    return _jsonify(stateObj.to_dict())
