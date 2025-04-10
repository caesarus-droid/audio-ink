import subprocess
import sys
import os

def install_requirements():
    # First install a basic version of torch to check for CUDA
    subprocess.check_call([sys.executable, "-m", "pip", "install", "torch==2.2.1"])
    
    # Now run the GPU check
    from check_gpu import check_cuda
    
    if check_cuda():
        print("Installing GPU requirements...")
        requirements_file = "requirements-gpu.txt"
    else:
        print("Installing CPU requirements...")
        requirements_file = "requirements-cpu.txt"
    
    # Install the appropriate requirements
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
    print(f"\nInstallation completed using {requirements_file}")

if __name__ == "__main__":
    install_requirements() 