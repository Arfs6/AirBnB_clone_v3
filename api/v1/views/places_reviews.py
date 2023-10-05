#!/usr/bin/python3
"""reviews endpoint"""

from flask import request, abort, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def allReviewsInPlace(place_id):
    """Returns a list of Review objects linked to a place."""
    placeObj = storage.get(Place, place_id)
    if not placeObj:
        abort(404)
    return jsonify([reviewObj.to_dict() for reviewObj in placeObj.reviews])


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def reviewById(review_id):
    """Returns the Review object with id = @review_id"""
    reviewObj = storage.get(Review, review_id)
    if reviewObj is None:
        abort(404)
    return reviewObj.to_dict()


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete Review object with id = @review_id"""
    reviewObj = storage.get(Review, review_id)
    if reviewObj is None:
        abort(404)
    reviewObj.delete()
    storage.save()
    return {}


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def newReview(place_id):
    """Creates a new Review.
    Info is in request json.
    """
    placeObj = storage.get(Place, place_id)
    if not placeObj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    elif 'user_id' not in data:
        abort(400, 'Missing user_id')
    userObj = storage.get(User, data['user_id'])
    if not userObj:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')
    reviewObj = Review()
    reviewObj.place_id = place_id
    for key, value in data.items():
        if key not in ['id', 'place_id', 'updated_at', 'created_at']:
            setattr(reviewObj, key, value)
    reviewObj.save()
    return reviewObj.to_dict(), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def updateReview(review_id):
    """Updates a User object with id @user_id
    returns the updated User object.
    """
    reviewObj = storage.get(Review, review_id)
    if reviewObj is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(reviewObj, key, value)
    reviewObj.save()
    return reviewObj.to_dict()
