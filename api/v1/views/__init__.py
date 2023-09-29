#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Flask blueprints for flask app."""
from flask import Blueprint


app_views = Blueprint('api', __name__, url_prefix='/api/v1')


from api.v1.views.index import *
