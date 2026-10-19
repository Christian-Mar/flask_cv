from dotenv import load_dotenv
from flask import Flask

from .config import Config
from .extensions import csrf


def create_app(config_class: type = Config) -> Flask:
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config_class)

    csrf.init_app(app)

    from .blueprints.public import bp as public_bp

    app.register_blueprint(public_bp)

    return app
