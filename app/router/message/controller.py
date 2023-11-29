import json
from flask import request
from flask_restx import Resource, Namespace

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt)

from app.service import message as msg_service
from app.service import user_bahave as behavior_service
from app.router.message.api_model import ApiModel
from app.router.decorate import token_required
from app.router.request import response

api = Namespace("message", description="chat message related operations")
model = ApiModel(api)
# logger = logging.getLogger("router")


@api.route("/message")
class MessageList(Resource):
    @api.doc("list_of_messages")
    # @api.marshal_list_with(_user, envelope='data')
    @jwt_required()
    def get(self):
        """List all registered users"""
        user_id = get_jwt_identity()
        latest_seq = request.args.get("seq")
        # access_token = create_access_token(identity=user_id)
        result = msg_service.get_user_messages(user_id,latest_seq)
        return response(data = result)

    @api.doc("post_one_message")
    @jwt_required()
    def post(self):
        message = request.args.get("message[text]")
        last_seq_string = request.args.get("last_seq")
        user_location = request.args.get("location")
        location_query = request.args.get("location_query")
        last_seq = int(last_seq_string)
        user_id = get_jwt_identity()
        ai_reply = msg_service.add_one_message(user_id, message,last_seq,user_location,location_query).to_dict()
        # add send message recording
        type = "send_message"
        data = {}
        data["message"] = message
        record = behavior_service.add_one_user_behaviour(user_id = user_id, type = type, data=json.dumps(data)).to_dict()
        return response(data = ai_reply)

    @api.doc("delete all messages")
    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        msg_service.delete_all_messages(user_id)
        return response(data = "success")
 #
    # @api.response(201, 'User successfully created.')
    # @api.doc('create a new user')
    # @api.expect(_user, validate=True)
    # def post(self):
    #     """Creates a new User """
    #     data = request.json
    #     return save_new_user(data=data)



@api.route("/test")
class TestApi(Resource):
    @api.expect(model.postModel, validate=True)
    @jwt_required()
    def get(self):
        rating = msg_service.get_product_rating("B0002F513E","1440957997408449281")
        print(rating)
        return response(data = "result")
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
