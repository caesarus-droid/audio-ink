from flask import Blueprint, request, jsonify, current_app
import yt_dlp
import os
import tempfile
from pathlib import Path
from .transcription import transcribe_audio
from app.models.transcription import Transcription
from datetime import datetime

youtube_api = Blueprint('youtube_api', __name__)

def download_youtube_audio(url: str) -> str:
    """Download audio from YouTube video."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            output_path = temp_file.name

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Unknown Title')
            return output_path, title

    except Exception as e:
        current_app.logger.error(f"Error downloading YouTube video: {str(e)}")
        if os.path.exists(output_path):
            os.unlink(output_path)
        raise Exception(f"Failed to download YouTube video: {str(e)}")

@youtube_api.route('/youtube/transcribe', methods=['POST'])
def transcribe_youtube():
    """Transcribe audio from a YouTube video."""
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # Download the YouTube video's audio
        audio_path, video_title = download_youtube_audio(url)

        # Transcribe the audio
        result = transcribe_audio(audio_path)

        if 'error' in result:
            raise Exception(result['error'])

        # Create transcription record
        transcription = Transcription(
            file_name=f"{video_title}.mp3",
            file_path=audio_path,
            text=result['text'],
            status='completed',
            processing_time=result['processing_time'],
            device=result['device'],
            language=result['language']
        )
        transcription.save()

        # Clean up the temporary file
        try:
            os.unlink(audio_path)
        except Exception as e:
            current_app.logger.warning(f"Error cleaning up temporary file: {str(e)}")

        return jsonify({
            'id': transcription.id,
            'title': video_title,
            'text': result['text'],
            'processing_time': result['processing_time']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500 