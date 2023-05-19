from flask_sqlalchemy import SQLAlchemy
from app.model import init_model
import logging

class DaoPool():

    sqlDAO = None
    esDAO = None

    def __init__(self):
        pass

    def init_app(self, app):
        # db init
        logging.getLogger("dao").info("init database")
        self.sqlDAO = SQLAlchemy(app)
        init_model(self.sqlDAO)
        logging.getLogger("dao").info("database init complete")


daoPool = DaoPool()