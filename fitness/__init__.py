from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from nutritionix import Nutritionix
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = '982b8f6e08e8cedff2c6deb24a40bbe6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Enable CORS for React frontend
CORS(app, origins=['http://localhost:3000', 'http://localhost:5173', 'http://localhost:5000'])

# Create database
db = SQLAlchemy(app)

# Password encryption
bcrypt = Bcrypt(app)

# Login manager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Nutritionix API
nix = Nutritionix(app_id=10908293, api_key="65ec9bee4c82e455f41d19c810f88f89")

# Register error handlers
from fitness.api.v1.middleware import register_error_handlers
register_error_handlers(app)

# Register API v1 routes
from fitness.api.v1.routes import register_api_v1
register_api_v1(app)

# Import legacy routes (for backward compatibility during migration)
from fitness import routes
