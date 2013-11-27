from flask import Flask
from webapp.database import init_db, create_all_table, create_all_test_table


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename, silent=True)

    init_db(app.config['SQLALCHEMY_DATABASE_URI'])

    if not app.config['DEBUG']:
        create_all_table()

    else:
        create_all_test_table()

    return app
