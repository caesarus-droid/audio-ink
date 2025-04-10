import os
from app import create_app, db
from app.models.user import User
from app.models.transcription import Transcription

app = create_app(os.getenv('FLASK_ENV', 'default'))

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Transcription=Transcription)

if __name__ == '__main__':
    if os.getenv('FLASK_ENV') == 'production':
        import gunicorn
        gunicorn.run(app, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
    else:
        app.run(debug=True) 