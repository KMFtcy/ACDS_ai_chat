import os

CONFIG_NAME_MAPPER = {
    'development': 'configDevelopment.cfg',
    'testing': 'configTesting.yaml',
    'production': 'configProduction.yaml'
}

class appConfig:

    def init_config(app, flask_config_name):
        ## Load Config
        env_flask_config_name = os.getenv('FLASK_CONFIG')
        if not env_flask_config_name and flask_config_name is None:
            flask_config_name = 'development'
        elif flask_config_name is None:
            flask_config_name = env_flask_config_name


        try:
            if CONFIG_NAME_MAPPER[flask_config_name] is None:
                return None
        except KeyError:
            return None

        app.config.from_pyfile(CONFIG_NAME_MAPPER[flask_config_name])
        app.config.SWAGGER_UI_JSONEDITOR = True
        app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

        return