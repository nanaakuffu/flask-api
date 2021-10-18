import logging
import sys
from typing import Dict
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
from flask_restful import Api

from src.api.resources.models.users import User, UserSchema

from .api.utils.database import db
from .api.utils.responses import Responses as R


from .api.resources.routes import Routes


class Application():
    """
    This is the application factory class that produces instances of the application.

    At its instantiation, it only accepts the configuration imported form the config class.
    """

    def __init__(self, config) -> None:
        self.config = config
        self.app = Flask(__name__)

        self.app.config.from_object(config)

        self.jwt = JWTManager(self.app)
        self.api = Api(self.app)

        self.middlewares()

        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

        logging.basicConfig(stream=sys.stdout,
                            format='%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)s]',
                            level=logging.DEBUG)

        logging.getLogger("pika").setLevel(logging.WARNING)

        self.configure_logging()

    def getCurrentUser(self):
        @self.jwt.user_lookup_loader
        def getUser(jwt_header: Dict, jwt_data: Dict):
            currentUser = User.findByEmail(jwt_data['sub'])
            userData = UserSchema().dump(currentUser)
            del userData['password']

            return userData

    def middlewares(self):
        CORS(self.app)

        Routes(self.api).routes()

        self.getCurrentUser()

        self.errorHandlers()

    def errorHandlers(self):
        @self.app.after_request
        def add_header(response):
            return response

        @self.app.errorhandler(400)
        def bad_request(e):
            logging.error(e)
            return R.response_with(R.BAD_REQUEST_400)

        @self.app.errorhandler(500)
        def server_error(e):
            logging.error(e)
            return R.response_with(R.SERVER_ERROR_500)

        @self.app.errorhandler(404)
        def not_found(e):
            logging.error(e)
            return R.response_with(R.SERVER_ERROR_404)

        @self.app.errorhandler(405)
        def method_not_allowed(e):
            logging.error(e)
            return R.response_with(R.METHOD_NOT_ALLOWED_405)

    def configure_logging(self):
        # Deactivate the default flask logger so that log messages don't get duplicated
        self.app.logger.removeHandler(default_handler)

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
        self.app.logger.addHandler(file_handler)
