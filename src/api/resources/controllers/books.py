from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource
from flask import request
from marshmallow.exceptions import ValidationError

from ..models.books import Book, BookSchema
from ...utils.responses import Responses
from ...utils.database import db


class BooksApi(Resource, Responses):
    def get(self):
        try:
            data = Book.query.all()
            book_schema = BookSchema(
                many=True, only=['id', 'title', 'year', 'author_id'])
            books = book_schema.dump(data)
            return self.response_with(self.SUCCESS_200, value=books)
        except Exception as e:
            print(e)
            return self.response_with(self.SERVER_ERROR_500)

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            book_schema = BookSchema()
            book_data = book_schema.load(data)

            book_data['author_id'] = current_user['id']
            book = Book(**book_data)

            result = book_schema.dump(book.create())

            return self.response_with(self.SUCCESS_201, value=result)
        except ValidationError as err:
            print(err)
            return self.response_with(self.INVALID_FIELD_NAME_SENT_422, error=err.messages)
        except Exception as e:
            print(e)
            return self.response_with(self.INVALID_INPUT_422)


class BookApi(Resource, Responses):
    def get(self, book_id):
        bookData = Book.query.get_or_404(book_id)
        try:
            result = BookSchema().dump(bookData)
            return self.response_with(self.SUCCESS_200, value=result)
        except Exception as e:
            print(e)
            return self.response_with(self.SERVER_ERROR_500)

    @jwt_required()
    def put(self, book_id):
        bookData = Book.query.get_or_404(book_id)
        try:
            data = request.get_json()
            book_schema = BookSchema()
            book_data = book_schema.load(data)
            bookData.title = book_data['title']
            bookData.year = book_data['year']

            db.session.add(bookData)
            db.session.commit()

            bookSchemaData = book_schema.dump(bookData)

            return self.response_with(self.SUCCESS_200, value=bookSchemaData)

        except ValidationError as err:
            print(err)
            return self.response_with(self.INVALID_FIELD_NAME_SENT_422, error=err)
        except Exception as e:
            print(e)
            return self.response_with(self.INVALID_INPUT_422)

    @jwt_required()
    def delete(self, book_id):
        bookData = Book.query.get_or_404(book_id)
        try:
            db.session.delete(bookData)
            db.session.commit()

            return self.response_with(self.SUCCESS_204)
        except Exception as e:
            print(e)
            return self.response_with(self.SERVER_ERROR_500)
