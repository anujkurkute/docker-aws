
"""
Database connection and initialization utilities.
"""

import os
from flask import Flask
from models import db


def init_db(app: Flask):
    """Configure and initialize Flask-SQLAlchemy."""

    database_url = os.environ.get('DATABASE_URL')

    if not database_url:
        db_user = os.environ.get('DB_USER', 'flaskuser')
        db_password = os.environ.get('DB_PASSWORD', 'flaskpass123')
        db_host = os.environ.get('DB_HOST', 'db')
        db_port = os.environ.get('DB_PORT', '5432')
        db_name = os.environ.get('DB_NAME', 'tasksdb')

        database_url = (
            f'postgresql://{db_user}:{db_password}'
            f'@{db_host}:{db_port}/{db_name}'
        )

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the extension only.
    # Do not create tables or insert sample data here.
    db.init_app(app)


def get_db_connection_info(app: Flask):
    return {
        'database_uri': app.config.get(
            'SQLALCHEMY_DATABASE_URI', 'Not set'
        ),
        'engine': str(db.engine.url) if db.engine else 'Not initialized'
    }
