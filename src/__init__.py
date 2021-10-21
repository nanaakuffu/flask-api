import logging
import sys
from typing import Dict
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
from flask_restful import Api
from flask_migrate import Migrate

from src.api.resources.models.users import User, UserSchema

from .api.utils.database import db, ma
from .api.utils.error_handler import ErrorHandler


from .api.routes.web import routes


class Application():
    """
    This is the application factory class that produces instances of the application.

    At its instantiation, it only accepts the configuration imported form the config class.
    """
    prefix = "/api/v1"

    def __init__(self, config) -> None:
        self.config = config
        self.app = Flask(__name__)

        self.app.config.from_object(config)

        self.jwt = JWTManager(self.app)
        self.api = Api(self.app)
        self.migrate = Migrate(self.app, db)

        db.init_app(self.app)
        ma.init_app(self.app)

        self.middlewares()

        logging.basicConfig(stream=sys.stdout,
                            format='%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)s]',
                            level=logging.DEBUG)

        logging.getLogger("pika").setLevel(logging.WARNING)

        self.configure_logging(self.app)

    def getCurrentUser(self):
        @self.jwt.user_lookup_loader
        def getUser(jwt_header: Dict, jwt_data: Dict):
            user = User.findByEmail(jwt_data['sub'])
            userData = UserSchema(
                only=['id', 'first_name', 'last_name', 'email', 'is_verified', 'created_at']).dump(user)

            return userData

    def middlewares(self):
        CORS(self.app)

        self.routes()

        self.getCurrentUser()

        errorHandler = ErrorHandler(self.app, self.jwt)
        errorHandler.errorHandlers()

    def routes(self):
        for route in routes:
            route['url'] = self.prefix+'/'+route['url']
            self.api.add_resource(
                route['resource'],
                route['url'],
                endpoint=route['endpoint'] if 'endpoint' in route else route['resource'].__name__.lower(
                )
            )

    def configure_logging(self, app):
        # Deactivate the default flask logger so that log messages don't get duplicated
        app.logger.removeHandler(default_handler)

        # Create a file handler object
        file_handler = RotatingFileHandler(
            'flaskapp.log', maxBytes=16384, backupCount=20)

        # Set the logging level of the file handler object so that it logs INFO and up
        file_handler.setLevel(logging.INFO)

        # Create a file formatter object
        file_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')

        # Apply the file formatter object to the file handler object
        file_handler.setFormatter(file_formatter)

        # Add file handler object to the logger
        app.logger.addHandler(file_handler)
