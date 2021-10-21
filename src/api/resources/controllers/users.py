from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required

from ..models.users import User, UserSchema
from ...utils.responses import Responses
from ...utils.email import EmailBroker
from ...utils.database import db
from ...utils.token import EmailVerificationToken
from ...utils.queues import Queues


class UsersApi(Resource, Responses):
    @jwt_required()
    def get(self):
        try:
            data = User.query.all()
            userSchema = UserSchema(
                many=True, only=['id', 'first_name', 'last_name', 'email', 'is_verified', 'created_at'])
            users = userSchema.dump(data)

            return self.response_with(self.SUCCESS_200, value=users)
        except Exception as e:
            print(e)
            return self.response_with(self.SERVER_ERROR_500)

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()

            if User.findByEmail(data['email']) is not None:
                return self.response_with(self.INVALID_INPUT_422)

            data['password'] = User.generateHash(data['password'])
            user_schema = UserSchema()
            user_data = user_schema.load(data)
            user = User(**user_data)

            # Send request to the queue to run in the background
            # queue = Queues()
            # queue.sendDispatch(data['email'])

            email = EmailBroker(current_app.config['SECRET_KEY'],
                                current_app.config['SECURITY_PASSWORD_SALT'])

            email.threadQueue(data['email'])

            result = user_schema.dump(user.create())
            del result['password']

            return self.response_with(self.SUCCESS_201, value=result)

        except Exception as e:
            print(e)
            return self.response_with(self.INVALID_INPUT_422)


class LoginApi(Resource, Responses):
    def __str__(self) -> str:
        return 'login'

    def post(self):
        try:
            data = request.get_json()
            user = User.findByEmail(data['email'])
            if not user:
                return self.response_with(self.CLIENT_ERROR_404)

            if user and not user.is_verified:

                # Send request to the queue to run in the background
                # Queues().sendDispatch(user.email)

                email = EmailBroker(current_app.config['SECRET_KEY'],
                                    current_app.config['SECURITY_PASSWORD_SALT'])

                email.threadQueue(user.email)

                return self.response_with(self.EMAIL_NOT_VERIFIED_400)

            if User.verifyHash(data['password'],
                               user.password
                               ):

                access_token = create_access_token(identity=data['email'])
                userData = UserSchema(
                    only=['id', 'first_name', 'last_name', 'email', 'is_verified', 'created_at']).dump(user)

                userData['token'] = access_token
                return self.response_with(self.SUCCESS_200, value=userData)
            else:
                return self.response_with(self.INVALID_LOGIN_CREDENTIALS)
        except Exception as e:
            print(e)
            return self.response_with(self.INVALID_INPUT_422)


class EmailVerificationApi(Resource, Responses):
    def get(self, token):
        try:
            verify_email = EmailVerificationToken(current_app.config['SECRET_KEY'],
                                                  current_app.config['SECURITY_PASSWORD_SALT'])
            email = verify_email.confirmVerificationToken(token)

            if not email:
                self.response_with(self.VERIFIVATION_TOKEN_EXPIRED_400)

            # print(email)
            user = User.query.filter_by(email=email).first_or_404()

            if not user.is_verified:
                user.is_verified = True
                db.session.add(user)
                db.session.commit()

                return self.response_with(self.EMAIL_VERIFIED_200)

        except Exception as e:
            print(e)
            return self.response_with(self.CLIENT_ERROR_404)
