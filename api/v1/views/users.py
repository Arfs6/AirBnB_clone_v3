#!/usr/bin/python3
"""users endpoint"""

from flask import request, abort, jsonify
import hashlib
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def getAllUsers():
    """Returns a list object containing all User objects."""
    allUsers = storage.all(User)
    return jsonify([userObj.to_dict() for userObj in allUsers.values()])


@app_views.route('/users/<user_id>', strict_slashes=False)
def userById(user_id):
    """Return user with id @user_id"""
    userObj = storage.get(User, user_id)
    if userObj is None:
        abort(404)
    return userObj.to_dict()


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteUserById(user_id):
    """Delete User object with id @user_id"""
    userObj = storage.get(User, user_id)
    if userObj is None:
        abort(404)
    userObj.delete()
    storage.save()
    return {}, 200


def hashPassword(password):
    """converts a password to an md5 hash."""
    md5Hash = hashlib.md5()
    md5Hash.update(password.encode('utf-8'))
    return md5Hash.hexdigest()


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def newUser():
    """Creates a new User.
    Info is in request json.
    """
    userInfo = request.get_json()
    if not userInfo:
        abort(400, 'Not a JSON')
    elif 'email' not in userInfo:
        abort(400, 'Missing email')
    elif 'password' not in userInfo:
        abort(400, 'Missing password')
    newUser = User()
    newUser.password = hashPassword(userInfo['password'])
    ignoreAttrs = ['id', 'created_at', 'updated_at', 'password']
    for key, value in userInfo.items():
        if key not in ignoreAttrs:
            setattr(newUser, key, value)
    newUser.save()
    return newUser.to_dict(), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def updateUser(user_id):
    """Updates a User object with id @user_id
    returns the updated User object.
    """
    userObj = storage.get(User, user_id)
    if userObj is None:
        abort(404)
    userInfo = request.get_json()
    if not userInfo:
        abort(400, 'Not a JSON')

    if 'password' in userInfo:
        userObj.password = hashPassword(userInfo.pop('password'))
    for key, value in userInfo.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(userObj, key, value)
    userObj.save()
    return userObj.to_dict()
