from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required

from ..models.users import User, UserSchema
from ...utils.responses import Responses as R
from ...utils.email import EmailBroker
from ...utils.database import db
from ...utils.token import EmailVerificationToken
from ...utils.queues import Queues


class UsersApi(Resource):
    @jwt_required()
    def get(self):
        try:
            data = User.query.all()
            userSchema = UserSchema(
                many=True, only=['id', 'first_name', 'last_name', 'email', 'is_verified', 'created_at'])
            users = userSchema.dump(data)

            return R.response_with(R.SUCCESS_200, value=users)
        except Exception as e:
            print(e)
            return R.response_with(R.SERVER_ERROR_500, error=e)

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()

            if User.findByEmail(data['email']) is not None:
                return R.response_with(R.INVALID_INPUT_422)

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

            return R.response_with(R.SUCCESS_201, value=result)

        except Exception as e:
            print(e)
            return R.response_with(R.INVALID_INPUT_422, error=e)


class LoginApi(Resource):
    def __str__(self) -> str:
        return 'login'

    def post(self):
        try:
            data = request.get_json()
            currentUser = User.findByEmail(data['email'])
            if not currentUser:
                return R.response_with(R.SERVER_ERROR_404)

            if currentUser and not currentUser.is_verified:

                # Send request to the queue to run in the background
                # Queues().sendDispatch(currentUser.email)

                email = EmailBroker(current_app.config['SECRET_KEY'],
                                    current_app.config['SECURITY_PASSWORD_SALT'])

                email.threadQueue(currentUser.email)

                return R.response_with(R.EMAIL_NOT_VERIFIED_400)

            if User.verifyHash(data['password'], currentUser.
                               password):

                access_token = create_access_token(identity=data['email'])
                userData = UserSchema().dump(currentUser)
                del userData['password']
                userData['token'] = access_token
                return R.response_with(R.SUCCESS_200, value=userData)
            else:
                return R.response_with(R.UNAUTHORIZED_401)
        except Exception as e:
            print(e)
            return R.response_with(R.INVALID_INPUT_422)


class EmailVerificationApi(Resource):
    def get(self, token):
        try:
            verify_email = EmailVerificationToken(current_app.config['SECRET_KEY'],
                                                  current_app.config['SECURITY_PASSWORD_SALT'])
            email = verify_email.confirmVerificationToken(token)

            if not email:
                R.response_with(R.VERIFIVATION_TOKEN_EXPIRED_400)

            # print(email)
            user = User.query.filter_by(email=email).first_or_404()
            if user.is_verified:
                return R.response_with(R.INVALID_INPUT_422)
            else:
                user.is_verified = True
                db.session.add(user)
                db.session.commit()

                return R.response_with(R.EMAIL_VERIFIED_200)
        except Exception as e:
            print(e)
            return R.response_with(R.SERVER_ERROR_404)
