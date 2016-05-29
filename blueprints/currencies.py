#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import jsonify, Blueprint
import pycountry

## currencies Blueprint ########################################################

currencies = Blueprint('currencies', __name__)

@currencies.route('/')
def get_currencies():
    result = {}
    for currency in pycountry.currencies:
        currency_dict_temp = {}
        currency_dict_temp['name'] = currency.name
        currency_dict_temp['letter'] = currency.letter
        try:
            currency_dict_temp['numeric'] = currency.numeric
        except:
            pass

        result[currency.name] = currency_dict_temp

    return jsonify(result), 200

@currencies.route('/<letter>')
def get_currency(letter):
    try:
        try:
            c = pycountry.currencies.get(letter=str(letter).upper())
        except:
            try:
                c = pycountry.currencies.get(numeric=str(letter).upper())
            except:
                c = pycountry.currencies.get(name=str(letter).upper())

        result = {}
        result['name'] = c.name
        result['numeric'] = c.numeric
        result['letter'] = c.letter

        return jsonify(result), 200
    except:
        return jsonify({'error': 'currency could not be found'})
