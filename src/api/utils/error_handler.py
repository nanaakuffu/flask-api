import logging
from .responses import Responses


class ErrorHandler(Responses):
    def __init__(self, app, jwt) -> None:
        self._app = app
        self._jwt = jwt

    def errorHandlers(self):
        @self._app.after_request
        def add_header(response):
            return response

        @self._jwt.expired_token_loader
        def token_expired(jwt_header, jwt_data):
            return self.response_with(self.JWT_TOKEN_EXPIRED_401)

        @self._jwt.invalid_token_loader
        def invalid_token(reason: str):
            return self.response_with(self.INVALID_TOKEN_401)

        @self._jwt.unauthorized_loader
        def no_token_header(reason: str):
            return self.response_with(self.TOKENLESS_HEADER_401)

        @self._app.errorhandler(400)
        def bad_request(e):
            logging.error(e)
            return self.response_with(self.BAD_REQUEST_400, error=e)

        @self._app.errorhandler(500)
        def server_error(e):
            logging.error(e)
            return self.response_with(self.SERVER_ERROR_500, error=e)

        @self._app.errorhandler(404)
        def not_found(e):
            logging.error(e)
            return self.response_with(self.CLIENT_ERROR_404, error=e)

        @self._app.errorhandler(405)
        def method_not_allowed(e):
            logging.error(e)
            return self.response_with(self.METHOD_NOT_ALLOWED_405, error=e)
