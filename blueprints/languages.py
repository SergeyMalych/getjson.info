#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import jsonify, Blueprint
import pycountry

## languages Blueprint ########################################################

languages = Blueprint('languages', __name__)

@languages.route('/')
def get_languages():
    result = {}
    for language in pycountry.languages:
        language_dict_temp = {}

        try:
            language_dict_temp['name'] = language.name
        except:
            pass
        try:
            language_dict_temp['inverted_name'] = language.inverted_name
        except:
            pass
        try:
            language_dict_temp['common_name'] = language.common_name
        except:
            pass
        try:
            language_dict_temp['iso639_1_code'] = language.iso639_1_code
        except:
            pass
        try:
            language_dict_temp['iso639_2T_code'] = language.iso639_2T_code
        except:
            pass
        try:
            language_dict_temp['iso639_3_code'] = language.iso639_3_code
        except:
            pass


        result[language.name] = language_dict_temp

    return jsonify(result), 200

@languages.route('/<code>')
def get_language(code):
    try:
        try:
            language = pycountry.languages.get(iso639_1_code=str(code).lower())
        except:
            try:
                language = pycountry.languages.get(iso639_2T_code=str(code).lower())
            except:
                language = pycountry.languages.get(iso639_3_code=str(code).lower())


        result = {}

        try:
            result['name'] = language.name
        except:
            pass
        try:
            result['common_name'] = language.common_name
        except:
            pass
        try:
            result['iso639_1_code'] = language.iso639_1_code
        except:
            pass
        try:
            result['iso639_2T_code'] = language.iso639_2T_code
        except:
            pass
        try:
            result['iso639_3_code'] = language.iso639_3_code
        except:
            pass

        return jsonify(result), 200
    except:
        return jsonify({'error': 'language could not be found'})
