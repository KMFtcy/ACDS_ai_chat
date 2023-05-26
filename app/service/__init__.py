import logging

logger = logging.getLogger("service")

class AppContext():
    config = None

    def __init__(self):
        pass

    def init_app(self, app):
        self.config = app.config

context = AppContext()