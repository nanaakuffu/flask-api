from itsdangerous import URLSafeTimedSerializer


class EmailVerificationToken():
    """
    A class to provide the token and token confirmation.

    It takes the secret key and salt. All are passed to it from the config.
    """

    def __init__(self, secret_key: str, salt: str) -> None:
        self.secret_key = secret_key
        self.salt = salt

    def generateVerificationToken(self, email: str) -> str:
        serializer = URLSafeTimedSerializer(secret_key=self.secret_key)
        return serializer.dumps(email, salt=self.salt)

    def confirmVerificationToken(self, token: str, expiration: int = 3600) -> str:
        serializer = URLSafeTimedSerializer(secret_key=self.secret_key)
        try:
            email = serializer.loads(token,
                                     salt=self.salt,
                                     max_age=expiration
                                     )

            return email
        except Exception as e:
            return e
