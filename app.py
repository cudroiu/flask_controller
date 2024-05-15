from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
import logging

from config import Config
from extensions import db
from models.wifi_status import WifiStatus
from resources.wifi_status import WifiStatusResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    logging.basicConfig(filename='/var/log/f_controller.log', encoding='utf-8', level=logging.DEBUG)
    register_extensions(app)
    register_resources(app)
    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)

def register_resources(app):
    api = Api(app)
    api.add_resource(WifiStatusResource, '/wifi', resource_class_kwargs={'logger': app.logger})

if __name__ == '__main__':
    app = create_app()
    app.run()