#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import jsonify, Blueprint, request
import hashlib

## hash Blueprint ################################################################

hash = Blueprint('hash', __name__)

@hash.route("/<userinput>")
def get_hash_by_parameter(userinput):
    try:
        userinput = userinput.encode('utf-8')
        return jsonify({'md5':hashlib.md5(userinput).hexdigest(),
            'sha1':hashlib.sha1(userinput).hexdigest(),
            'sha224':hashlib.sha224(userinput).hexdigest(),
            'sha256':hashlib.sha256(userinput).hexdigest(),
            'sha384':hashlib.sha384(userinput).hexdigest(),
            'sha512':hashlib.sha512(userinput).hexdigest()}), 200
        #for proxy:
        # request.environ.get('HTTP_X_REAL_hash', request.remote_addr)
    except Exception as ex:
        return jsonify({'error': 'fail hashing', 'ex':ex})