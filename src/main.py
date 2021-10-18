# import logging
# import os
# import sys
# from threading import Thread
# from flask import Flask, jsonify
# from flask.cli import with_appcontext
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager
# from api.config.config import DevelopmentConfig, ProductionConfig, TestingConfig

# from api.utils.database import db
# from api.utils.queues import Queues
# from api.utils.responses import response_with
# import api.utils.responses as resp
# from api.utils.email import EmailBroker

# from api.routes.authors import author_routes
# from api.routes.books import book_routes
# from api.routes.users import user_routes


# class Application():

#     def __init__(self, config) -> None:
#         self.config = config
#         self.app = Flask(__name__)

#         self.app.config.from_object(config)

#         jwt = JWTManager(self.app)

#         # db.init_app(self.app)
#         # with self.app.app_context():
#         #     db.create_all()

#         self.middlewares()

#         db.init_app(self.app)
#         with self.app.app_context():
#             db.create_all()

#         logging.basicConfig(stream=sys.stdout,
#                             format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s',
#                             level=logging.DEBUG)

#         logging.getLogger("pika").setLevel(logging.WARNING)

#     def middlewares(self):
#         CORS(self.app)

#         self.routes()

#         @self.app.after_request
#         def add_header(response):
#             return response

#         @self.app.errorhandler(400)
#         def bad_request(e):
#             logging.error(e)
#             return response_with(resp.BAD_REQUEST_400)

#         @self.app.errorhandler(500)
#         def server_error(e):
#             logging.error(e)
#             return response_with(resp.SERVER_ERROR_500)

#         @self.app.errorhandler(404)
#         def not_found(e):
#             logging.error(e)
#             return response_with(resp.SERVER_ERROR_404)

#         @self.app.errorhandler(405)
#         def method_not_allowed(e):
#             logging.error(e)
#             return response_with(resp.METHOD_NOT_ALLOWED_405)

#     def routes(self):
#         self.app.register_blueprint(
#             author_routes, url_prefix='/api/v1/authors')
#         self.app.register_blueprint(book_routes, url_prefix='/api/v1/books')
#         self.app.register_blueprint(user_routes, url_prefix='/api/v1/users')


# def create_app(config):
#     app = Flask(__name__)

#     app.config.from_object(config)

#     CORS(app)

#     app.register_blueprint(author_routes, url_prefix='/api/v1/authors')
#     app.register_blueprint(book_routes, url_prefix='/api/v1/books')

#     @app.after_request
#     def add_header(response):
#         return response

#     @app.errorhandler(400)
#     def bad_request(e):
#         logging.error(e)
#         return response_with(resp.BAD_REQUEST_400)

#     @app.errorhandler(500)
#     def server_error(e):
#         logging.error(e)
#         return response_with(resp.SERVER_ERROR_500)

#     @app.errorhandler(404)
#     def not_found(e):
#         logging.error(e)
#         return response_with(resp.SERVER_ERROR_404)

#     @app.errorhandler(405)
#     def method_not_allowed(e):
#         logging.error(e)
#         return response_with(resp.METHOD_NOT_ALLOWED_405)

#     db.init_app(app)
#     with app.app_context():
#         db.create_all()

#     logging.basicConfig(stream=sys.stdout,
#                         format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s',
#                         level=logging.DEBUG)

#     return app


# # if os.environ.get('WORK_ENV') == 'PROD':
# #     app_config = ProductionConfig
# # elif os.environ.get('WORK_ENV') == 'TEST':
# #     app_config = TestingConfig
# # else:
# #     app_config = DevelopmentConfig


# # # application = create_app(app_config)
# # application = Application(app_config).app

# # with application.app_context():
# #     channel = Queues('localhost').receiveDispatch()
# #     thread = Thread(target=channel.start_consuming)
# #     thread.start()


# # if __name__ == '__main__':
# #     application.run(port=1122, debug=True)
