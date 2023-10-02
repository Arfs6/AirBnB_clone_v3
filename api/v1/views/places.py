#!/usr/bin/python3
"""places endpoints"""

from flask import request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def allPlacesInCity(city_id):
    """Returns a list of all Places
    in a City with id = @city_id
    """
    cityObj = storage.get(City, city_id)
    if not cityObj:
        abort(404)
    return [placeObj.to_dict() for placeObj in cityObj.places]


@app_views.route('/places/<place_id>', strict_slashes=False)
def placeById(place_id):
    """Returns a Place object with id = @place_id"""
    placeObj = storage.get(Place, place_id)
    if placeObj is None:
        abort(404)
    return placeObj.to_dict()


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlaceById(place_id):
    """Deletes the Place object with id = @place_id"""
    placeObj = storage.get(Place, place_id)
    if placeObj is None:
        abort(404)
    placeObj.delete()
    storage.save()
    return {}


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def newPlace(city_id):
    """Creates a new Place object."""
    cityObj = storage.get(City, city_id)
    if not cityObj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    elif 'user_id' not in data:
        abort(400, 'Missing user_id')
    userObj = storage.get(User, data['user_id'])
    if not userObj:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    newPlace = Place()
    newPlace.city_id = city_id
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'city_id']:
            # including user_id
            setattr(newPlace, key, value)
    newPlace.save()
    return newPlace.to_dict(), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def updatePlace(place_id):
    """Updates the Place object with id = @place_id"""
    placeObj = storage.get(Place, place_id)
    if placeObj is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(placeObj, key, value)
    placeObj.save()
    return placeObj.to_dict(), 200


@app_views.route('/places_search', methods=['post'],
           strict_slashes=False)
def searchPlace():
    """Search for places"""
    data = request.get_json()
    if data is None:
        abort(404)
    if not data or (
        not data.get('states')
        and not data.get('cities')
        and not data.get('amenities')
    ):
        return [obj.to_dict() for obj in storage.all(Place).values()]
    citiesSet = set()
    if data.get('states'):
        for stateId in data.get('states'):
            stateObj = storage.get(State, stateId)
            if not stateObj:
                abort(404)
            citiesSet.update({cityObj for cityObj in stateObj.cities})
    if data.get('cities'):
        for cityId in data.get('id'):
            cityObj = storage.get(City, cityId)
            if not cityObj:
                abort(404)
            citiesSet.add(cityObj)
    placesList = [cityObj.places for cityObj in citiesSet]
    if data.get('amenities'):
        if not data.get('states') and not data.get('cities'):
            placesList = list(storage.all(Place).values())
        amenities = [storage.get(Amenity, amenityId) for amenityId in data.get('amenities')]
        copiedPlaces = placesList.copy()
        for placeObj in copiedPlaces:
            if not all(amenity in placeObj.amenities for amenity in amenities):
                placesList.remove(placeObj)

    return [placeObj.to_dict() for placeObj in placesList]
