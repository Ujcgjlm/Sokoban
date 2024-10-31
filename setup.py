import subprocess
import sys

def install_requirements():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    except subprocess.CalledProcessError:
        print("Failed to install requirements.")
        sys.exit(1)

def run_application():
    try:
        subprocess.check_call([sys.executable, 'main.py'])
    except subprocess.CalledProcessError:
        print("Failed to run the application.")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()
    run_application()
