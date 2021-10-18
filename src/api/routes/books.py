from flask import Blueprint, request

from ..utils.responses import response_with
from ..utils import responses as resp
from ..resources.models.books import Book, BookSchema
from ..utils.database import db

book_routes = Blueprint('book_routes', __name__)


@book_routes.route('/', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        try:
            data = Book.query.all()
            book_schema = BookSchema(
                many=True, only=['id', 'title', 'year', 'author_id'])
            books = book_schema.dump(data)
            return response_with(resp.SUCCESS_200, value=books)
        except Exception as e:
            print(e)
            return response_with(resp.SERVER_ERROR_500)
    else:
        try:
            data = request.get_json()
            book_schema = BookSchema()
            book_data = book_schema.load(data)
            book = Book(**book_data)

            result = book_schema.dump(book.create())

            return response_with(resp.SUCCESS_201, value=result)
        except Exception as e:
            print(e)
            print(book)
            return response_with(resp.INVALID_INPUT_422)


@book_routes.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def bookById(id):
    bookData = Book.query.get_or_404(id)
    if request.method == 'GET':
        try:
            result = BookSchema().dump(bookData)
            return response_with(resp.SUCCESS_200, value=result)
        except Exception as e:
            print(e)
            return response_with(resp.SERVER_ERROR_500)
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            bookData.title = data['title']
            bookData.year = data['year']

            db.session.add(bookData)
            db.session.commit()

            bookSchemaData = BookSchema().dump(bookData)

            return response_with(resp.SUCCESS_200, value=bookSchemaData)

        except Exception as e:
            print(e)
            return response_with(resp.INVALID_INPUT_422)
    else:
        try:
            db.session.delete(bookData)
            db.session.commit()

            return response_with(resp.SUCCESS_204)
        except Exception as e:
            print(e)
            return response_with(resp.SERVER_ERROR_500)
