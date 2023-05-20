from flask_restx import Api, Resource, fields
from app.router import message as msgRouter
import logging

logger = logging.getLogger("dao")

class AppApi():
    api = None

    def __init__(self):
        pass

    def init_api(self, app):
        self.api = Api(app, version='1.0', title='TodoMVC API',
            description='A simple TodoMVC API',
        )
        self.api.add_namespace(msgRouter.api, path='/message')
        return

appApi = AppApi()