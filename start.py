import subprocess
import sys
import os
import venv

def check_python():
    try:
        subprocess.run(['python', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        print("Python is not installed. Please install Python and try again.")
        sys.exit(1)

def create_venv():
    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        venv.create('venv', with_pip=True)
    else:
        print("Virtual environment already exists.")

def install_dependencies():
    print("Installing dependencies...")
    subprocess.run(['venv\\Scripts\\activate.bat', '&&', 'pip', 'install', '-r', 'requirements.txt'], shell=True, check=True)

def start_main():
    print("Starting main.py...")
    subprocess.run(['venv\\Scripts\\activate.bat', '&&', 'python', 'src\\main.py'], shell=True, check=True)

def main():
    check_python()
    create_venv()
    install_dependencies()
    start_main()

if __name__ == "__main__":
    main()
