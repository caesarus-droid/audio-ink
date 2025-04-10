from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
import os
import torch

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .api.transcription import api as transcription_api
    app.register_blueprint(transcription_api, url_prefix='/api')

    # Create necessary directories
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)
    os.makedirs(app.config.get('STORAGE_PATH', 'storage'), exist_ok=True)
    os.makedirs(app.config.get('MODEL_PATH', 'models'), exist_ok=True)

    # Root route
    @app.route('/')
    def index():
        return render_template('index.html')

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
