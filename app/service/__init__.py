import logging
from app.utils import chat

logger = logging.getLogger("service")

class AppContext():
    config = None

    def __init__(self):
        pass

    def init_app(self, app):
        # load configuration
        self.config = app.config
        # init openai engine
        chat.init_products(app.config["ACDS_PRODUCT_DATA_PATH"])

context = AppContext()