from flask import Blueprint, request, current_app
from flask_jwt_extended import create_access_token, jwt_required
from threading import Thread

from ..resources.models.books import User, UserSchema

from src.api.utils.responses import response_with
from src.api.utils import responses as resp
from src.api.utils.database import db
from src.api.utils.token import EmailVerificationToken
from src.api.utils.email import EmailBroker

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/', methods=['GET', 'POST'])
@jwt_required()
def users():
    if request.method == 'GET':
        try:
            data = User.query.all()
            userSchema = UserSchema(
                many=True, only=['id', 'first_name', 'last_name', 'email', 'created_at'])
            users = userSchema.dump(data)
            return response_with(resp.SUCCESS_200, value=users)
        except Exception as e:
            print(e)
            return response_with(resp.SERVER_ERROR_500, error=e)
    else:
        try:
            data = request.get_json()

            if User.findByEmail(data['email']) is not None:
                return response_with(resp.INVALID_INPUT_422)

            data['password'] = User.generateHash(data['password'])
            user_schema = UserSchema()
            user_data = user_schema.load(data)
            user = User(**user_data)

            # Send email to rabbitmq server
            # thred = Thread(target=sendVerificationEmail, args=[data['email']])
            # thred.start()
            # Queues('localhost').sendDispatch(data['email'])
            # sendVerificationEmail(email=data['email'])

            result = user_schema.dump(user.create())
            del result['password']

            return response_with(resp.SUCCESS_201, value=result)

        except Exception as e:
            print(e)
            return response_with(resp.INVALID_INPUT_422, error=e)


@user_routes.route('/auth/login', methods=['POST'])
def authenticateUser():
    try:
        data = request.get_json()
        currentUser = User.findByEmail(data['email'])
        if not currentUser:
            return response_with(resp.SERVER_ERROR_404)

        if currentUser and not currentUser.is_verified:

            email = EmailBroker()

            thread = Thread(target=email.sendVerificationEmail,
                            args=[currentUser.email])
            thread.start()
            # sendVerificationEmail(email=currentUser.email)
            return response_with(resp.EMAIL_NOT_VERIFIED_400)

        if User.verifyHash(data['password'], currentUser.
                           password):

            access_token = create_access_token(identity=data['email'])
            userData = UserSchema().dump(currentUser)
            del userData['password']
            userData['token'] = access_token
            return response_with(resp.SUCCESS_201, value=userData)
        else:
            return response_with(resp.UNAUTHORIZED_401)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@user_routes.route('/confirm/<token>', methods=['GET'])
def verifyEmail(token):
    try:
        verify_email = EmailVerificationToken(current_app.config['SECRET_KEY'],
                                              current_app.config['SECURITY_PASSWORD_SALT'])
        email = verify_email.confirmVerificationToken(token)

        print(email)
        user = User.query.filter_by(email=email).first_or_404()
        if user.is_verified:
            return response_with(resp.INVALID_INPUT_422)
        else:
            user.is_verified = True
            db.session.add(user)
            db.session.commit()

            return response_with(resp.EMAIL_VERIFIED_200)
    except Exception as e:
        print(e)
        return response_with(resp.SERVER_ERROR_404)
