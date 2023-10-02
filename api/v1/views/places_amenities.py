#!/usr/bin/python3
"""End point for the link between amenities and places"""

from flask import request, abort
from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route('places/<place_id>/amenities', strict_slashes=False)
def allAmenitiesInPlace(place_id):
    """Returns a list of all amenities in a place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if storage_t == "db":
        amenities = [amenityObj.to_dict() for amenityObj in place.amenities]
    else:
        amenities = [
            storage.get(Amenity, amenity_id).to_dict()
            for amenity_id in place.amenity_ids
        ]

    return amenities


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def deleteAmenityInPlace(place_id, amenity_id):
    """Deletes an Amenity in A place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenityObj = storage.get(Amenity, amenity_id)
    if not amenityObj:
        abort(404)

    if storage_t == "db":
        if amenityObj not in place.amenities:
            abort(404)
        place.amenities.remove(amenityObj)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return {}


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def linkPlaceWithAmenity(place_id, amenity_id):
    """Add an amenity in a place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage_t == "db":
        if amenity in place.amenities:
            return amenity.to_dict()
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return amenity.to_dict()
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return amenity.to_dict(), 201
