import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
import urllib.request
import zipfile
import tempfile

def check_python_version():
    """Check if Python version meets requirements"""
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    if current_version < required_version:
        print(f"Error: Python {required_version[0]}.{required_version[1]} or higher is required")
        sys.exit(1)
    print(f"✓ Python {current_version[0]}.{current_version[1]} detected")

def create_virtual_environment():
    """Create and activate virtual environment"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    else:
        print("Virtual environment already exists")

def get_venv_python():
    """Get the path to the virtual environment's Python executable"""
    if platform.system() == "Windows":
        return Path("venv/Scripts/python.exe")
    else:
        return Path("venv/bin/python")

def install_requirements():
    """Install dependencies based on GPU availability"""
    python_path = get_venv_python()
    
    # First install a basic version of torch to check for CUDA
    print("Installing basic torch to check for GPU...")
    subprocess.check_call([str(python_path), "-m", "pip", "install", "torch==2.2.1"])
    
    # Check for CUDA
    import torch
    if torch.cuda.is_available():
        print("✓ CUDA GPU detected!")
        print(f"Device: {torch.cuda.get_device_name(0)}")
        requirements_file = "requirements-gpu.txt"
    else:
        print("No CUDA GPU detected. Using CPU version.")
        requirements_file = "requirements-cpu.txt"
    
    # Install requirements
    print(f"Installing dependencies from {requirements_file}...")
    subprocess.check_call([str(python_path), "-m", "pip", "install", "-r", requirements_file])

def setup_ffmpeg():
    """Set up FFmpeg based on the operating system"""
    system = platform.system()
    
    if system == "Windows":
        # Check if FFmpeg is already in PATH
        if shutil.which("ffmpeg"):
            print("✓ FFmpeg is already installed")
            return
            
        print("Downloading FFmpeg for Windows...")
        ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "ffmpeg.zip")
        
        try:
            # Download FFmpeg
            urllib.request.urlretrieve(ffmpeg_url, zip_path)
            
            # Extract FFmpeg
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find the bin directory
            bin_dir = None
            for root, dirs, files in os.walk(temp_dir):
                if "ffmpeg.exe" in files:
                    bin_dir = root
                    break
            
            if bin_dir:
                # Add to PATH
                os.environ["PATH"] = bin_dir + os.pathsep + os.environ["PATH"]
                print("✓ FFmpeg installed and added to PATH")
            else:
                print("Error: Could not find FFmpeg executable in downloaded files")
        except Exception as e:
            print(f"Error installing FFmpeg: {e}")
        finally:
            # Clean up
            shutil.rmtree(temp_dir)
            
    elif system == "Darwin":  # macOS
        try:
            subprocess.check_call(["brew", "install", "ffmpeg"])
            print("✓ FFmpeg installed via Homebrew")
        except subprocess.CalledProcessError:
            print("Error: Could not install FFmpeg via Homebrew")
            
    elif system == "Linux":
        try:
            subprocess.check_call(["sudo", "apt-get", "install", "-y", "ffmpeg"])
            print("✓ FFmpeg installed via apt-get")
        except subprocess.CalledProcessError:
            print("Error: Could not install FFmpeg via apt-get")

def setup_environment():
    """Set up environment variables"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if not env_file.exists():
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print("✓ Created .env file from .env.example")
        else:
            print("Warning: .env.example not found")
    else:
        print("✓ .env file already exists")

def initialize_database():
    """Initialize the database"""
    python_path = get_venv_python()
    try:
        print("Initializing database...")
        subprocess.check_call([str(python_path), "-m", "flask", "db", "init"])
        subprocess.check_call([str(python_path), "-m", "flask", "db", "migrate"])
        subprocess.check_call([str(python_path), "-m", "flask", "db", "upgrade"])
        print("✓ Database initialized successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing database: {e}")

def main():
    print("Starting AudioInk setup...")
    
    # Check system requirements
    check_python_version()
    
    # Create virtual environment
    create_virtual_environment()
    
    # Install requirements
    install_requirements()
    
    # Set up FFmpeg
    setup_ffmpeg()
    
    # Set up environment
    setup_environment()
    
    # Initialize database
    initialize_database()
    
    print("\nSetup completed successfully!")
    print("\nTo start the application:")
    print("1. Activate the virtual environment:")
    if platform.system() == "Windows":
        print("   .\\venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Run the application:")
    print("   python run.py")
    print("\nThe application will be available at http://localhost:5000")

if __name__ == "__main__":
    main() 