from flask_sqlalchemy import model
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, Schema

from .books import BookSchema
from ...utils.database import db


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    books = db.relationship('Book', backref='Author',
                            cascade="all, delete-orphan")
    avatar = db.Column(db.String(20), nullable=True)

    def __init__(self, first_name: str = None, last_name: str = None, books=[]) -> None:
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.books = books

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class AuthorSchema(Schema):
    class Meta(Schema.Meta):
        # fields = ('id', 'first_name', 'last_name', 'books')
        model = Author
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    created_at = fields.String(dump_only=True)
    books = fields.Nested(BookSchema, many=True,
                          only=['title', 'year', 'id'])
    avatar = fields.String(dump_only=True)
