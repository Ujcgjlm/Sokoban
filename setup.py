import subprocess
import sys
import os
import venv
from pathlib import Path

def create_venv():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        venv.create(venv_path, with_pip=True)
    return venv_path

def get_venv_python():
    """Get path to Python executable in virtual environment"""
    if sys.platform == "win32":
        return str(Path("venv/Scripts/python.exe"))
    return str(Path("venv/bin/python"))

def install_requirements(python_path):
    """Install requirements using venv Python"""
    try:
        subprocess.check_call([python_path, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    except subprocess.CalledProcessError:
        print("Failed to install requirements.")
        sys.exit(1)

def run_application(python_path):
    """Run application using venv Python"""
    try:
        subprocess.check_call([python_path, 'main.py'])
    except subprocess.CalledProcessError:
        print("Failed to run the application.")
        sys.exit(1)

if __name__ == "__main__":
    venv_path = create_venv()
    python_path = get_venv_python()
    install_requirements(python_path)
    run_application(python_path)
