#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import jsonify, Blueprint, request
import pygeoip

## IP Blueprint ################################################################

ip = Blueprint('ip', __name__)

gic = pygeoip.GeoIP(r'./GeoLiteCity.dat')

@ip.route("/")
def get_ip():
    try:
        try:
            geo = gic.record_by_addr(request.access_route[0])
            if not geo:
                raise
        except:
            geo = 'geolocation could not be found'
        return jsonify({'ip': request.access_route[0],
            'geo': geo}), 200
        #for proxy:
        # request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    except:
        return jsonify({'error': 'ip could not be found'})

@ip.route("/<address>")
def get_ip_by_parameter(address):
    try:
        try:
            geo = gic.record_by_addr(address)
            name = 'ip'
        except:
            geo = gic.record_by_name(address)
            name = 'address'
        return jsonify({name: address,
            'geo': geo}), 200
        #for proxy:
        # request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    except:
        return jsonify({'error': 'address could not be found'})