#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Index resource of api."""

from json import dumps
from flask import make_response
from api.v1.views import app_views
import models


@app_views.route('/status')
def status():
    """Checks if server is still up."""
    response = make_response(dumps({
        'status': 'OK',
    },
                 indent=2))
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/stats')
def stats():
    """Get some stats."""
    data = {}
    data['amenities'] = models.storage.count(models.amenity.Amenity)
    data['cities'] = models.storage.count(models.city.City)
    data['places'] = models.storage.count(models.place.Place)
    data['reviews'] = models.storage.count(models.review.Review)
    data['states'] = models.storage.count(models.state.State)
    data['users'] = models.storage.count(models.user.User)
    response = make_response(dumps(data, indent=2))
    response.headers['Content-Type'] = 'application/json'
    return response
