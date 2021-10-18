from threading import Thread
from flask import current_app
from flask.helpers import url_for
from flask.templating import render_template_string
from flask_mail import Message, Mail

from .token import EmailVerificationToken


class EmailBroker():
    def __init__(self, secret_key: str, salt: str) -> None:
        self.app = current_app._get_current_object()
        self.mail = Mail(self.app)
        self.verify_email = EmailVerificationToken(secret_key=secret_key,
                                                   salt=salt)
        self._default_sender = self.app.config['MAIL_DEFAULT_SENDER']

    def sendEmail(self,
                  to: str,
                  subject: str,
                  template: str):
        with self.mail.connect() as connection:
            message = Message(
                subject=subject,
                recipients=[to],
                html=template,
                sender=self._default_sender
            )

            connection.send(message=message)

    def sendVerificationEmail(self,
                              email: str):
        token = self.verify_email.generateVerificationToken(email=email)

        with self.app.app_context():
            verificationEmail = url_for('confirm_email',
                                        token=token,
                                        _external=True)

        template = ""
        with self.app.open_resource('files/email_template.txt', 'r') as f:
            for line in f:
                template += line

        with self.app.app_context():
            html = render_template_string(template,
                                          verification_email=verificationEmail)

            subject = "Email Verification"
            self.sendEmail(
                to=email,
                subject=subject,
                template=html
            )

    def threadQueue(self, email: str):
        thread = Thread(target=self.sendVerificationEmail,
                        args=[email])
        thread.start()
