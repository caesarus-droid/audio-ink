from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import Config
import os
import torch

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from .routes import bp as main_bp
    from .routes.auth import auth
    from .api.transcription import api as transcription_api
    from .api.youtube import youtube_api
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(transcription_api, url_prefix='/api/transcription')
    app.register_blueprint(youtube_api, url_prefix='/api/youtube')

    # Create necessary directories
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)
    os.makedirs(app.config.get('STORAGE_PATH', 'storage'), exist_ok=True)
    os.makedirs(app.config.get('MODEL_PATH', 'models'), exist_ok=True)

    # Health check endpoint
    @app.route('/health')
    def health_check():
        try:
            # Check database connection
            db.session.execute('SELECT 1')
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'gpu': 'available' if torch.cuda.is_available() else 'unavailable'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'error': str(e)
            }), 500

    return app

# User loader for Flask-Login
@login_manager.user_loader
def load_user(id):
    from .models.user import User
    return User.query.get(int(id))
