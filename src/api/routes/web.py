from ..resources.controllers.authors import AuthorApi, AuthorAvatarApi, AuthorsApi
from ..resources.controllers.books import BookApi, BooksApi
from ..resources.controllers.users import EmailVerificationApi, LoginApi, UsersApi

routes = [
    {
        "resource": UsersApi,
        "url": 'users'
    },

    # Books routes
    {
        "resource": BooksApi,
        "url": "books"
    },
    {
        "resource": BookApi,
        "url": "books/<int:book_id>"
    },

    # Author routes
    {
        "resource": AuthorsApi,
        "url": "authors"
    },
    {
        "resource": AuthorApi,
        "url": "authors/<int:author_id>"
    },
    {
        "resource": AuthorAvatarApi,
        "url": "avatar/<int:author_id>"
    },

    # Login route
    {
        "resource": LoginApi,
        "url": "auth/login"
    },

    # Email verification route
    {
        "resource": EmailVerificationApi,
        "url": "confirm/<token>",
        "endpoint": "confirm_email"
    },
]
