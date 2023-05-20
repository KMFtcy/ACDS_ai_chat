import logging
from flask import Flask
from flask_cors import CORS, cross_origin


def create_app(flask_config_name=None):
    """' create flask app"""

    ## Creat app
    app = Flask(__name__)

    ## init config
    from app.config import appConfig

    appConfig.init_config(app, flask_config_name)

    # CORS(app, reousrces={r'/api/*':{"origins":app.config['CORS_ORIGIN']}})

    ## Set logger
    # logging.getLogger('flask_cors').level = logging.DEBUG
    # logging.getLogger('elasticsearch').level = logging.WARNING
    logging.basicConfig(
        format=app.config["LOGGER_FORMAT"], level=app.config["LOGGER_LEVEL"]
    )

    ## DB init
    from app.dao import daoPool

    daoPool.init_app(app)

    ## Api init
    from app.api import appApi
    appApi.init_api(app)

    return app
