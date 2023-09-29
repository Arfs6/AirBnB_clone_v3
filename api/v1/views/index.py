#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Index resource of api."""

from json import dumps
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Checks if server is still up."""
    return dumps({
        'status': 'OK',
    },
                 indent=2)
