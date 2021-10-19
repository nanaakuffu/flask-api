from jinja2.loaders import FileSystemLoader
from passlib.hash import pbkdf2_sha256 as sha256
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from src.api.utils.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True,
                      nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    is_verified = db.Column(db.Boolean, nullable=False, default=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def findByEmail(cls, email):
        return cls.query.filter_by(email=email).first()

    @staticmethod
    def generateHash(password):
        return sha256.hash(password)

    @staticmethod
    def verifyHash(password, hash):
        return sha256.verify(password, hash)


class UserSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = User
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    created_at = fields.String(dump_only=True)
    is_verified = fields.Integer(dump_only=True)
