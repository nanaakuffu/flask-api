from typing import Any, Dict
from flask import make_response, jsonify, Response


class Responses():

    INVALID_FIELD_NAME_SENT_422 = {
        "http_code": 422,
        "code": "invalidField",
        "message": "Invalid fields found"
    }

    INVALID_INPUT_422 = {
        "http_code": 422,
        "code": "invalidInput",
        "message": "Invalid input"
    }

    MISSING_PARAMETERS_422 = {
        "http_code": 422,
        "code": "missingParameter",
        "message": "Missing parameters."
    }

    BAD_REQUEST_400 = {
        "http_code": 400,
        "code": "badRequest",
        "message": "Bad request"
    }

    EMAIL_NOT_VERIFIED_400 = {
        "http_code": 400,
        "code": "emailBadRequest",
        "message": "Email not verified. A verification link has been sent to your email."
    }

    VERIFIVATION_TOKEN_EXPIRED_400 = {
        "http_code": 400,
        "code": "verificationTokenExpired",
        "message": "Email verification token has expired."
    }

    EMAIL_NOT_VERIFIED_500 = {
        "http_code": 500,
        "code": "serverEmailBadRequest",
        "message": "Verification email was not sent. Please recheck your email address and try again."
    }

    METHOD_NOT_ALLOWED_405 = {
        "http_code": 405,
        "code": "methodNotAllowed",
        "message": "Method not allowed"
    }

    SERVER_ERROR_500 = {
        "http_code": 500,
        "code": "serverError",
        "message": "Internal Server Error"
    }

    SERVER_ERROR_404 = {
        "http_code": 404,
        "code": "notFound",
        "message": "Resource not found"
    }

    UNAUTHORIZED_403 = {
        "http_code": 403,
        "code": "notAuthorized",
        "message": "You are not authorised to execute this."
    }

    SUCCESS_200 = {
        'http_code': 200,
        'code': 'success',
        'message': 'Request completed successfully'
    }
    SUCCESS_201 = {
        'http_code': 201,
        'code': 'success',
        'message': 'Request completed successfully'
    }

    SUCCESS_204 = {
        'http_code': 204,
        'code': 'success',
        'message': 'Request completed successfully'
    }

    EMAIL_VERIFIED_200 = {
        "http_code": 200,
        "code": "badRequest",
        "message": "Email verified, you can proceed to login now."
    }

    @staticmethod
    def response_with(
        response: Dict,
        value: Any = None,
        message: str = None,
        error: Any = None,
        headers: Dict = {},
        pagination: Any = None
    ) -> Response:
        result = {}
        if value is not None:
            result.update({'data': value})

        if response.get('message', None) is not None:
            result.update({'message': response['message']})

        if response.get('http_code', None) is not None:
            result.update({'status_code': response['http_code']})

        if error is not None:
            result.update({'errors': error})

        if pagination is not None:
            result.update({'pagination': pagination})

        # headers.update({'Access-Control-Allow-Origin': '*'})
        headers.update({'Server': 'Flask REST API'})

        return make_response(jsonify(result), response['http_code'], headers)
