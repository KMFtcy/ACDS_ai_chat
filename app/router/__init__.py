from flask_restx import Api
from flask import url_for
from app.router.message.controller import api as msgRouter
import logging
import urllib

from flask_jwt_extended import JWTManager
logger = logging.getLogger("router")

class AppApi():
    api = None

    def __init__(self):
        pass

    def init_api(self, app):
        self.api = Api(app, version='1.0', title='TodoMVC API',
            description='A simple TodoMVC API',
        )
        self.api.add_namespace(msgRouter, path='/chat/message')
        jwt = JWTManager(app)

        # print router
        for url in app.url_map.iter_rules():
            logger.info(url)
        return

appApi = AppApi()