from dynaconf.contrib import FlaskDynaconf
from flask import Flask
from flask_rest_api import Api
from flask import Flask
from flask import request
import logging
import os, sys

from app.config import app_config

env_mode = os.environ['ENV_MODE']

sys.path.append(os.path.dirname(__file__) + os.sep + './')

def register_blueprints(app, *blps):
    api = Api(app=app)
    for blp in blps:
        api.register_blueprint(blp)

    return api


def create_app(config_module):
    app = Flask(__name__)
    app.config.from_object(config_module)

    # make app.config support dot notation.
    FlaskDynaconf(app=app)

    # register blueprints
    from app.router import user_api, pair_api
    register_blueprints(app, user_api)
    register_blueprints(app, pair_api)

    return app

app = create_app('app.config.' + app_config[env_mode])

if __name__ == '__main__':
    app.run()