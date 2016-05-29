#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import jsonify, Blueprint
import pycountry

## countries Blueprint ########################################################

countries = Blueprint('countries', __name__)

@countries.route('/')
def get_countries():
    result = {}
    for country in pycountry.countries:
        country_dict_temp = {}
        country_dict_temp['name'] = country.name
        country_dict_temp['numeric'] = country.numeric
        country_dict_temp['alpha2'] = country.alpha2
        country_dict_temp['alpha3'] = country.alpha3
        try:
            country_dict_temp['official_name'] = country.official_name
        except:
            pass

        result[country.name] = country_dict_temp

    return jsonify(result), 200

@countries.route('/<country>')
def get_country(country):
    try:
        try:
            c = pycountry.countries.get(alpha2=str(country).upper())
        except:
            try:
                c = pycountry.countries.get(alpha3=str(country).upper())
            except:
                try:
                    c = pycountry.countries.get(numeric=str(country).upper())
                except:
                    c = pycountry.countries.get(name=str(country).upper())
                    
        result = {}
        result['name'] = c.name
        result['numeric'] = c.numeric
        result['alpha2'] = c.alpha2
        result['alpha3'] = c.alpha3
        try:
            result['official_name'] = c.official_name
        except:
            pass

        return jsonify(result), 200
    except:
        return jsonify({'error': 'country code could not be found'})
