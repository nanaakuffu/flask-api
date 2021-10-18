from flask_restful import Api
from .controllers.users import EmailVerificationApi, LoginApi, UsersApi
from .controllers.authors import AuthorApi, AuthorAvatarApi, AuthorsApi
from .controllers.books import BookApi, BooksApi


class Routes():
    """
    This is an object that defines all the routes within the application. 

    At instantiation, it takes the Api instance created in the Application class.

    The main method is the routes method, which puts all the routes together for easy recognition
    """

    def __init__(self, api: Api) -> None:
        self.api = api
        self.prefix = "/api/v1"

    def routes(self):
        # Books routes
        self.api.add_resource(BooksApi, f"{self.prefix}/books")
        self.api.add_resource(BookApi, f"{self.prefix}/books/<int:book_id>")

        # Author routes
        self.api.add_resource(AuthorsApi, f"{self.prefix}/authors")
        self.api.add_resource(AuthorApi,
                              f"{self.prefix}/authors/<int:author_id>")
        self.api.add_resource(AuthorAvatarApi,
                              f"{self.prefix}/avatar/<int:author_id>")

        # User routes
        self.api.add_resource(UsersApi, f"{self.prefix}/users")

        # Login route
        self.api.add_resource(LoginApi, f"{self.prefix}/auth/login")

        # Email verification route
        self.api.add_resource(EmailVerificationApi,
                              f"{self.prefix}/confirm/<token>", endpoint="confirm_email")
