import jwt

@staticmethod
def jwt_decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        key = "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"
        payload = jwt.decode(auth_token, key)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

# @staticmethod
# def get_logged_in_user(new_request):
#         # get the auth token
#         auth_token = new_request.headers.get('Authorization')
#         if auth_token:
#             resp = decode_auth_token(auth_token)
#             if not isinstance(resp, str):
#                 user = User.query.filter_by(id=resp).first()
#                 response_object = {
#                     'status': 'success',
#                     'data': {
#                         'user_id': user.id,
#                         'email': user.email,
#                         'admin': user.admin,
#                         'registered_on': str(user.registered_on)
#                     }
#                 }
#                 return response_object, 200
#             response_object = {
#                 'status': 'fail',
#                 'message': resp
#             }
#             return response_object, 401
#         else:
#             response_object = {
#                 'status': 'fail',
#                 'message': 'Provide a valid auth token.'
#             }
#             return response_object, 401