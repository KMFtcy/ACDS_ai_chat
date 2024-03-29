import json

from flask import request
from flask_restx import Resource, Namespace

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, decode_token)

from app.service import user_bahave as behavior_service
from app.router.user_behave.api_model import ApiModel
from app.router.decorate import token_required
from app.router.request import response

api = Namespace("user_behave", description="user behavior")
model = ApiModel(api)
# logger = logging.getLogger("router")


@api.route("/")
class Behaviour(Resource):
    @api.doc("list_of_one_user_behaviour")
    # @api.marshal_list_with(_user, envelope='data')
    @jwt_required()
    def get(self):
        # get user id
        user_id = get_jwt_identity()
        # get all behaviour data by ID
        result = behavior_service.get_user_behaviour(user_id)
        return response(data = result)

    @api.doc("add_one_behaviour")
    @jwt_required()
    def post(self):
        # get user id
        user_id = get_jwt_identity()
        # get behaviour record information
        type = request.args.get("type")
        data = request.args.get("data")
        # add to database
        record = behavior_service.add_one_user_behaviour(user_id = user_id, type = type, data=data).to_dict()
        return response(data =record)

@api.route("/quit")
class QuitBehaviorApi(Resource):
    @api.doc("add_quit_behaviour")
    def post(self):
        # get behaviour record information
        token = request.args.get("token")
        type = request.args.get("type")
        data = request.args.get("data")
        # {'userContext': '{"username":"testtest","nickName":"testtest","id":"1661789496733331456","longTerm":false,"role":"MEMBER","isSuper":false,"type":1}', 'sub': '1661789496733331456', 'type': 1, 'exp': 2060402096, 'fresh': False, 'jti': None}
        user_info = decode_token(encoded_token=token)
        user_id = json.loads(user_info["userContext"])["id"]
        record = behavior_service.add_one_user_behaviour(user_id = user_id, type = type, data=data).to_dict()
        # data = request.args.get("data")
        # add to database
        return response(data ={})

@api.route("/test")
class TestApi(Resource):
    @api.expect(model.postModel, validate=True)
    @jwt_required()
    def get(self):
        print("get it")
        print(api.payload)
        print("read it")
        return response(data = "result")