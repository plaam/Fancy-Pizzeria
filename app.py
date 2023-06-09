from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_principal import Principal

from flask_session import Session
from src.apis import register_blueprints
from src.context import db
from src.filters import load_filters
from src.handlers import (
    login_manager,
    load_identity_when_session_exists,
    register_error_handlers,
)

load_dotenv()

app = Flask(__name__, template_folder='templates', static_url_path="/static")
app.config.from_object('config.Config')

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)
Session(app)

login_manager.init_app(app)
principals = Principal(app)

load_identity_when_session_exists(app)
load_filters(app)

register_error_handlers(app)
register_blueprints(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
