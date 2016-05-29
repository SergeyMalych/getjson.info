#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import jsonify, Blueprint, request
import random

## random Blueprint ################################################################

rand = Blueprint('random', __name__)

@rand.route("/")
def get_ip():
    try:
        data = {'float': random.random(),
            'binary': random.randint(0,1),
            'digit': random.randint(0,9),
            'char': random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            'int': random.randint(0,9999999999999),
            'color': {'r':random.randint(0,255),
                'g':random.randint(0,255),
                'b':random.randint(0,255)}
            }
        return jsonify(data), 200
    except Exception as ex:
        return jsonify({'error': 'unknown'})