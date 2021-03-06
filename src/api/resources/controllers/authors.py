import os
from flask import request, current_app, send_from_directory
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource, abort
from werkzeug.utils import secure_filename
from marshmallow import ValidationError

from ..models.authors import Author, AuthorSchema
from ...utils.functions import Helpers as H
from ...utils.responses import Responses
from ...utils.database import db


class AuthorsApi(Resource, Responses):
    def get(self):
        try:
            data = Author.query.all()
            authorSchema = AuthorSchema(
                many=True)
            authors = authorSchema.dump(data)
            return self.response_with(self.SUCCESS_200, value=authors)
        except Exception as e:
            print(e)
            return self.response_with(self.SERVER_ERROR_500)

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            author_schema = AuthorSchema()

            author_data = author_schema.load(data)
            author = Author(**author_data)

            result = author_schema.dump(author.create())

            return self.response_with(self.SUCCESS_201, value=result)
        except ValidationError as err:
            print(err)
            return self.response_with(self.INVALID_FIELD_NAME_SENT_422, error=err.messages)
        except Exception as e:
            print(e)
            return self.response_with(self.INVALID_INPUT_422)


class AuthorApi(Resource, Responses):
    @jwt_required()
    def get(self, author_id):
        authorData = Author.query.get_or_404(author_id)
        try:
            # print(current_user['id'])
            author = AuthorSchema().dump(authorData)
            return self.response_with(self.SUCCESS_200, value=author)
        except Exception as e:
            print(e)
            return self.response_with(self.SERVER_ERROR_500)

    @jwt_required()
    def put(self, author_id):
        authorData = Author.query.get_or_404(author_id)
        try:
            data = request.get_json()
            authorData.first_name = data['first_name']
            authorData.last_name = data['last_name']

            db.session.add(authorData)
            db.session.commit()

            authorSchemaData = AuthorSchema().dump(authorData)

            return self.response_with(self.SUCCESS_200, value=authorSchemaData)
        except Exception as e:
            print(e)
            return self.response_with(self.INVALID_INPUT_422)

    @jwt_required()
    def delete(self, author_id):
        authorData = Author.query.get_or_404(id)

        try:
            db.session.delete(authorData)
            db.session.commit()

            return self.response_with(self.SUCCESS_204)
        except Exception as e:
            print(e)
            return self.response_with(self.SERVER_ERROR_500)


class AuthorAvatarApi(Resource):
    allowed_extensions = set(['image/jpeg', 'image/png', 'jpg'])

    def allowedFile(self, file_type):
        return file_type in self.allowed_extensions

    def get(self, author_id: int):
        upload_dir = os.path.join(
            os.getcwd(), current_app.config['UPLOAD_FOLDER'])

        author = Author.query.get_or_404(author_id)

        return send_from_directory(upload_dir, author.avatar)

    @jwt_required()
    def post(self, author_id: int):
        upload_dir = os.path.join(
            os.getcwd(), current_app.config['UPLOAD_FOLDER'])

        try:
            file = request.files['avatar']
            author = Author.query.get_or_404(author_id)

            if file and self.allowedFile(file.content_type):
                filename = H.hashString(upload_dir,
                                        'authors', secure_filename(file.filename))
                file.save(os.path.join(upload_dir, filename))

            author.avatar = filename

            db.session.add(author)
            db.session.commit()

            author_schema = AuthorSchema()
            author_data = author_schema.dump(author)

            return self.response_with(self.SUCCESS_200, value=author_data)
        except Exception as e:
            print(e)
            return self.response_with(self.INVALID_INPUT_422)
