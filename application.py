import os

from threading import Thread

from src import Application
from src.api.utils.email import EmailBroker
from config.config import ProductionConfig, TestingConfig, DevelopmentConfig
from src.api.utils.queues import Queues


if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

application = Application(app_config)

app = application.app

# Monitor and listen for queues changes
# with app.app_context():
#     email = EmailBroker(app.config['SECRET_KEY'],
#                         app.config['SECURITY_PASSWORD_SALT'])
#     channel = Queues(target=email.sendVerificationEmail).receiveDispatch()
#     thread = Thread(target=channel.start_consuming)
#     thread.start()


if __name__ == '__main__':
    app.run(port=1122)
