from flask_restx import Api, Resource, fields
# from app.api.message.apiController import api as ns1
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
        return

appApi = AppApi()