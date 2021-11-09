from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
# db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # app.config['SECRET_KEY'] = 'secret-key-goes-here'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config.from_pyfile('config.cfg')

    # db.init_app(app)

    # login_manager = LoginManager()
    # login_manager.login_view = 'routes.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(user_id):
    #     # since the user_id is just the primary key of our user table, use it in the query for the user
    #     return 1

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .routes import routes as main_blueprint
    app.register_blueprint(main_blueprint)

    return app