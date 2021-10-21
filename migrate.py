from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.api.utils.database import db
from application import app

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
