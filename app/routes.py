from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from .config import Config
from .models.transcription import Transcription
from .models.user import User
from flask_login import login_required, current_user
from . import db

bp = Blueprint('main', __name__)

# Template Routes
@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/transcript')
@login_required
def transcript():
    return render_template('transcript.html')

@bp.route('/youtube')
@login_required
def youtube():
    return render_template('youtube.html')

@bp.route('/history')
@login_required
def history():
    transcriptions = Transcription.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', transcriptions=transcriptions)

# API Routes
@bp.route('/api/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Create transcription record
        transcription = Transcription(
            user_id=current_user.id,
            filename=filename,
            status='processing'
        )
        db.session.add(transcription)
        db.session.commit()
        
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename,
            'transcription_id': transcription.id
        }), 200

@bp.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200 