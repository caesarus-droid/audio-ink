from flask import Blueprint

bp = Blueprint('main', __name__)

# Import routes after creating the blueprint to avoid circular imports
from app.routes import main
from app.routes import auth 