from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource
from flask import request

from ..models.books import Book, BookSchema
from ...utils.responses import Responses as R
from ...utils.database import db


class BooksApi(Resource):
    def get(self):
        try:
            data = Book.query.all()
            book_schema = BookSchema(
                many=True, only=['id', 'title', 'year', 'author_id'])
            books = book_schema.dump(data)
            return R.response_with(R.SUCCESS_200, value=books)
        except Exception as e:
            print(e)
            return R.response_with(R.SERVER_ERROR_500)

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            book_schema = BookSchema()
            book_data = book_schema.load(data)

            book_data['author_id'] = current_user['id']
            book = Book(**book_data)

            result = book_schema.dump(book.create())

            return R.response_with(R.SUCCESS_201, value=result)
        except Exception as e:
            print(e)
            return R.response_with(R.INVALID_INPUT_422)


class BookApi(Resource):
    def get(self, book_id):
        bookData = Book.query.get_or_404(book_id)
        try:
            result = BookSchema().dump(bookData)
            return R.response_with(R.SUCCESS_200, value=result)
        except Exception as e:
            print(e)
            return R.response_with(R.SERVER_ERROR_500)

    @jwt_required()
    def put(self, book_id):
        bookData = Book.query.get_or_404(book_id)
        try:
            data = request.get_json()
            bookData.title = data['title']
            bookData.year = data['year']

            db.session.add(bookData)
            db.session.commit()

            bookSchemaData = BookSchema().dump(bookData)

            return R.response_with(R.SUCCESS_200, value=bookSchemaData)

        except Exception as e:
            print(e)
            return R.response_with(R.INVALID_INPUT_422)

    @jwt_required()
    def delete(self, book_id):
        bookData = Book.query.get_or_404(book_id)
        try:
            db.session.delete(bookData)
            db.session.commit()

            return R.response_with(R.SUCCESS_204)
        except Exception as e:
            print(e)
            return R.response_with(R.SERVER_ERROR_500)
