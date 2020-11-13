from flask import Flask
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_principal import Principal
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
import os

login_manager = LoginManager()
db = SQLAlchemy()
admin = Admin()
principal = Principal()
migrate = Migrate()
app = Flask(__name__)

def create_app():

    app.config['SECRET_KEY'] = 'A SECRET KEY'

    POSTGRES = {
        'user': 'postgres',
        'pw': 'primavera',
        'db': 'Trivia',
        'host': '127.0.0.1',
        'port': '5432',
    }
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    BASE_DIR = os.path.dirname(__file__)

    MEDIA_URL = '/imagenes/'
    MEDIA_ROOT = os.path.join(BASE_DIR, "imagenes")

    login_manager.init_app(app)
    db.init_app(app)

    principal.init_app(app)

    # Se inicializa el objeto migrate
    migrate.init_app(app, db)
    bootstrap = Bootstrap(app)

    # Registro de los Blueprints
    from .errors import errors_bp
    app.register_blueprint(errors_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .restricted import restricted_bp
    app.register_blueprint(restricted_bp)

    return app