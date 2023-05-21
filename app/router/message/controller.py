from flask import request
from flask_restx import Resource, Namespace

from app.service import message as msg_service
from app.router.message.api_model import ApiModel
from app.router.decorate import token_required

import logging

api = Namespace("message", description="chat message related operations")
model = ApiModel(api)
# logger = logging.getLogger("router")


@api.route("/")
class UserList(Resource):
    @api.doc("list_of_registered_users")
    # @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        # return get_all_users()
        return "success"

    # @api.response(201, 'User successfully created.')
    # @api.doc('create a new user')
    # @api.expect(_user, validate=True)
    # def post(self):
    #     """Creates a new User """
    #     data = request.json
    #     return save_new_user(data=data)


@api.route("/test")
class TestApi(Resource):
    @api.expect(model, validate=True)
    @token_required
    def get(self,user_id):
        print("user_id: " + user_id)
        return "success"
# @api.route('/<public_id>')
# @api.param('public_id', 'The User identifier')
# @api.response(404, 'User not found.')
# class User(Resource):
#     @api.doc('get a user')
#     @api.marshal_with(_user)
#     def get(self, public_id):
#         """get a user given its identifier"""
#         user = get_a_user(public_id)
#         if not user:
#             api.abort(404)
#         else:
#             return user
#             return user
