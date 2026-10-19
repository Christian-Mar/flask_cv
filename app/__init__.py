from dotenv import load_dotenv
from flask import Flask

from .config import Config
from .extensions import csrf, init_mongo, login_manager


def create_app(config_class: type = Config) -> Flask:
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_mongo(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from .blueprints.admin import bp as admin_bp
    from .blueprints.public import bp as public_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    return app
