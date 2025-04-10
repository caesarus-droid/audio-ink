from flask import request, jsonify, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from app.routes import bp
from app.config import Config
from app.models.transcription import Transcription
from app.models.user import User
from flask_login import login_required, current_user
from app import db

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
    try:
        transcriptions = Transcription.query.filter_by(user_id=current_user.id).all()
        return render_template('history.html', transcriptions=transcriptions)
    except Exception as e:
        flash(f'Error loading history: {str(e)}', 'error')
        return redirect(url_for('main.index'))

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
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            # Create transcription record
            transcription = Transcription(
                user_id=current_user.id,
                filename=filename,
                status='pending'
            )
            db.session.add(transcription)
            db.session.commit()
            
            return jsonify({
                'message': 'File uploaded successfully',
                'transcription_id': transcription.id
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500 