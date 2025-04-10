from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
import os
import torch

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Create necessary directories
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)
    os.makedirs(app.config.get('STORAGE_PATH', 'storage'), exist_ok=True)
    os.makedirs(app.config.get('MODEL_PATH', 'models'), exist_ok=True)

    # Root route
    @app.route('/')
    def index():
        return render_template('index.html')

    # Transcribe route
    @app.route('/transcribe')
    def transcribe():
        return render_template('index.html')

    # YouTube route
    @app.route('/youtube')
    def youtube():
        return render_template('youtube.html')

    # History route
    @app.route('/history')
    def history():
        return render_template('history.html')

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
