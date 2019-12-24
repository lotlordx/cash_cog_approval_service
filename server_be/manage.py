from flask_script import Manager
from flask_migrate import MigrateCommand
from settings.constants import ENVIROMENT
from app import create_app

app = create_app(ENVIROMENT)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
