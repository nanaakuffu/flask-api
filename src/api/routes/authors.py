import os
from flask import Blueprint, request, url_for, current_app
# from flask.helpers import make_response
from flask import send_from_directory
# from flask_cors.core import try_match
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required

from ..utils.responses import Responses as R
from ..utils import responses as resp
from ..resources.models import Author, AuthorSchema
from src.api.utils.database import db
from src.api.utils.functions import hashString

author_routes = Blueprint("author_routes", __name__)

allowed_extensions = set(['image/jpeg', 'image/png', 'jpg'])


def allowedFile(file_type):
    return file_type in allowed_extensions


@author_routes.route('/', methods=['GET', 'POST'])
def authors():
    if request.method == 'GET':
        try:
            data = Author.query.all()
            authorSchema = AuthorSchema(
                many=True, only=['id', 'first_name', 'last_name', 'books', 'avatar'])
            authors = authorSchema.dump(data)
            return response_with(resp.SUCCESS_200, value=authors)
        except Exception as e:
            print(e)
            return response_with(resp.SERVER_ERROR_500)
    else:
        try:
            data = request.get_json()
            author_schema = AuthorSchema()
            author_data = author_schema.load(data)
            author = Author(**author_data)

            result = author_schema.dump(author.create())

            return response_with(resp.SUCCESS_201, value=result)
        except Exception as e:
            print(e)
            return response_with(resp.INVALID_INPUT_422)


@author_routes.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def authorById(id: int):
    authorData = Author.query.get_or_404(id)
    if request.method == 'GET':
        try:
            author = AuthorSchema(
                only=['id', 'first_name', 'last_name', 'books', 'avatar']).dump(authorData)
            return response_with(resp.SUCCESS_200, value=author)
        except Exception as e:
            print(e)
            return response_with(resp.SERVER_ERROR_500)

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            authorData.first_name = data['first_name']
            authorData.last_name = data['last_name']

            db.session.add(authorData)
            db.session.commit()

            authorSchemaData = AuthorSchema().dump(authorData)

            return response_with(resp.SUCCESS_200, value=authorSchemaData)
        except Exception as e:
            print(e)
            return response_with(resp.INVALID_INPUT_422)
    else:
        try:
            db.session.delete(authorData)
            db.session.commit()

            return response_with(resp.SUCCESS_204)
        except Exception as e:
            print(e)
            return response_with(resp.SERVER_ERROR_500)


@author_routes.route('/avatar/<int:author_id>', methods=['POST'])
@jwt_required()
def uploadAuthorAvatar(author_id):
    upload_dir = os.path.join(os.getcwd(), current_app.config['UPLOAD_FOLDER'])

    try:
        file = request.files['avatar']
        author = Author.query.get_or_404(author_id)

        if file and allowedFile(file.content_type):
            filename = hashString(upload_dir,
                                  'authors', secure_filename(file.filename))
            file.save(os.path.join(upload_dir, filename))

        author.avatar = filename

        db.session.add(author)
        db.session.commit()

        author_schema = AuthorSchema()
        author_data = author_schema.dump(author)

        return response_with(resp.SUCCESS_200, value=author_data)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@author_routes.route('/avatar/<int:author_id>')
def downloadFile(author_id):
    upload_dir = os.path.join(
        os.getcwd(), current_app.config['UPLOAD_FOLDER'])

    author = Author.query.get_or_404(author_id)

    return send_from_directory(upload_dir, author.avatar)
