from functools import wraps
from flask import request, jsonify

from app.auth.auth_helper import jwt_decode_auth_token

import jwt

key = "this_is_the_key_for_JWT"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.split(' ')[1]

        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            user_jwt = jwt.decode(token,key,algorithms='HS256')
            # current_user = User.query\
            #     .filter_by(public_id = data['public_id'])\
            #     .first()
        except Exception as e:
            print(e)
            return "something error"
        # returns the current logged in users context to the routes
        return  f(user_jwt, *args, **kwargs)

    return decorated

