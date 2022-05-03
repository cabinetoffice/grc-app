import os
from datetime import datetime, timedelta
from dateutil import tz
from flask import Flask
from flask_migrate import Migrate
from flask_uuid import FlaskUUID
from grc.models import db
from grc.config import Config, DevConfig, TestConfig
from grc.utils.s3 import download_object_data

migrate = Migrate()
flask_uuid = FlaskUUID()


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if os.environ['FLASK_ENV'] == 'production':
        config_object = Config
    elif os.environ['FLASK_ENV'] == 'development':
        config_object = DevConfig
    else:
        config_object = TestConfig

    app.config.from_object(config_object)

    # database
    db.init_app(app)
    migrate.init_app(app, db)

    flask_uuid.init_app(app)

    # update session timeout time
    @app.before_request
    def make_before_request():
        app.permanent_session_lifetime = timedelta(minutes=int(config_object.PERMANENT_SESSION_LIFETIME))

    # Filters
    @app.template_filter('format_date')
    def format_date_filter(dt):
        if dt:
            dt = dt.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))
            return datetime.strftime(dt, '%d/%m/%Y %H:%M')
        return ''

    @app.template_filter('image_data')
    def image_data_filter(image_name):
        if image_name:
            data, width, height = download_object_data(image_name)
            return data
        return ''

    @app.template_filter('image_width')
    def image_width_filter(image_name):
        if image_name:
            data, width, height = download_object_data(image_name)
            width, height = check_image_sizes(width, height)

            return width
        return ''

    @app.template_filter('image_height')
    def image_height_filter(image_name):
        if image_name:
            data, width, height = download_object_data(image_name)
            width, height = check_image_sizes(width, height)

            return height
        return ''

    def check_image_sizes(width, height):

        # Check sizes...595 x 842 pt
        ratio = 1.
        if width > 580:
            ratio = 580 / width
        elif height > 800:
            ratio = 800 / height
        width *= ratio
        height *= ratio
        return int(width), int(height)


    # Admin page
    from admin.admin import admin
    app.register_blueprint(admin)
    app.add_url_rule('/', endpoint='index')

    # Signout
    from admin.signout import signout
    app.register_blueprint(signout)
    app.add_url_rule('/signout', endpoint='index')

    # Password reset
    from admin.password_reset import password_reset
    app.register_blueprint(password_reset)
    app.add_url_rule('/password_reset', endpoint='index')

    # Forgot password
    from admin.forgot_password import forgot_password
    app.register_blueprint(forgot_password)
    app.add_url_rule('/forgot_password', endpoint='index')

    # Applications
    from admin.applications import applications
    app.register_blueprint(applications)
    app.add_url_rule('/applications', endpoint='index')

    # Manage users
    from admin.users import users
    app.register_blueprint(users)
    app.add_url_rule('/users', endpoint='index')

    # View security codes
    from admin.security_codes import codes
    app.register_blueprint(codes)
    app.add_url_rule('/security_codes', endpoint='index')

    return app
