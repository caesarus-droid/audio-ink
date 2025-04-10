# AudioInk

AudioInk instantly transforms your audio and video into accurate, ready-to-use transcripts using OpenAI's Whisper large-v3 model. Perfect for creators, educators, and professionals who need fast, reliable text from spoken content.

## Features

- Drag and drop interface for easy file upload
- Support for multiple audio formats (MP3, WAV, OGG, MP4, M4A, MPEG, WEBM)
- High-accuracy transcription using Whisper large-v3 model
- Local processing - no data leaves your machine
- Clean, modern Material UI design
- User authentication and management
- Rich text editor for transcript editing
- Export to Word documents
- Docker support with GPU acceleration

## Prerequisites

### Local Development
- Python 3.8 or higher
- FFmpeg
- CUDA-capable GPU (optional, for faster processing)
- PostgreSQL 12 or higher

### Docker Development
- Docker Engine 20.10.0 or higher
- Docker Compose 2.0.0 or higher
- NVIDIA Container Toolkit (for GPU support)
- NVIDIA Driver 450.80.02 or higher

## Installation

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/audio-ink.git
cd audio-ink
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install FFmpeg (required for audio processing):
- Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html) and add to PATH
- macOS: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg`

5. Install CUDA (optional, for GPU acceleration):
- Windows: Download and install from [NVIDIA website](https://developer.nvidia.com/cuda-downloads)
- macOS: `brew install cuda`
- Linux: Follow instructions on [NVIDIA website](https://developer.nvidia.com/cuda-downloads)

6. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

7. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

### Docker Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/audio-ink.git
cd audio-ink
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Build and start the containers:
```bash
docker-compose up --build
```

4. Initialize the database:
```bash
docker-compose exec web flask db init
docker-compose exec web flask db migrate
docker-compose exec web flask db upgrade
```

## Development

### Local Development
1. Start the Flask application:
```bash
python run.py
```

2. Open your web browser and navigate to `http://localhost:5000`

### Docker Development
1. Start the containers:
```bash
docker-compose up
```

2. Open your web browser and navigate to `http://localhost:5000`

## Production Deployment

### Local Deployment
1. Set up PostgreSQL:
```bash
createdb audioink_prod
```

2. Configure environment variables:
```bash
export FLASK_ENV=production
export DATABASE_URL=postgresql://username:password@localhost/audioink_prod
export SECRET_KEY=your-secret-key-here
```

3. Initialize the database:
```bash
flask db upgrade
```

4. Start the application:
```bash
gunicorn run:app
```

### Docker Deployment
1. Build and start the containers:
```bash
docker-compose -f docker-compose.yml up -d
```

2. The application will be available at `http://your-server:5000`

## System Requirements

### Local Development
- Python 3.8 or higher
- 16GB RAM minimum (32GB recommended)
- 10GB free disk space for the model
- FFmpeg installed
- CUDA-capable GPU (optional, for faster processing)
- PostgreSQL 12 or higher

### Docker Development
- Docker Engine 20.10.0 or higher
- Docker Compose 2.0.0 or higher
- NVIDIA Container Toolkit
- NVIDIA Driver 450.80.02 or higher
- 16GB RAM minimum (32GB recommended)
- 10GB free disk space

## Development

The application is built using:
- Flask for the backend
- Material UI for the frontend
- OpenAI Whisper for transcription
- PyTorch for machine learning
- PostgreSQL for data storage
- SQLAlchemy for ORM
- Gunicorn for production server
- Docker for containerization
- NVIDIA CUDA for GPU acceleration

### Project Structure

```
audio-ink/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── user.py
│   │   └── transcription.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── transcription.py
│   └── templates/
│       ├── index.html
│       └── transcript.html
├── config.py
├── requirements.txt
├── run.py
├── Dockerfile
├── docker-compose.yml
├── Procfile
├── .env.example
├── .gitignore
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
