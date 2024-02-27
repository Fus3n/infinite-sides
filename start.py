import subprocess
import sys
import os
import venv

def check_python():
    """    Check if Python is installed on the system.

    This function checks if Python is installed on the system by running the command 'python --version' using subprocess.
    If Python is not installed, it raises a CalledProcessError and prints a message to install Python.


    Raises:
        CalledProcessError: If the 'python --version' command fails.
    """

    try:
        subprocess.run(['python', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        print("Python is not installed. Please install Python and try again.")
        sys.exit(1)

def create_venv():
    """    Create a virtual environment if it does not exist already.

    If the virtual environment directory 'venv' does not exist, it creates a new virtual environment
    using the venv module. If the directory already exists, it prints a message indicating that the
    virtual environment already exists.
    """

    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        venv.create('venv', with_pip=True)
    else:
        print("Virtual environment already exists.")

def install_dependencies():
    """    Install dependencies using pip from requirements.txt file.

    This function activates the virtual environment and uses pip to install the required dependencies listed in the
    requirements.txt file.

    Raises:
        CalledProcessError: If the subprocess call to pip install fails.
    """

    print("Installing dependencies...")
    subprocess.run(['venv\\Scripts\\activate.bat', '&&', 'pip', 'install', '-r', 'requirements.txt'], shell=True, check=True)

def start_main():
    """    Start the main.py script.

    This function prints a message indicating the start of main.py and then runs the main.py script using a subprocess.

    Raises:
        CalledProcessError: If the subprocess call to run main.py fails.
    """

    print("Starting main.py...")
    subprocess.run(['venv\\Scripts\\activate.bat', '&&', 'python', 'src\\main.py'], shell=True, check=True)

def main():
    """    Main function to execute the necessary steps for setting up and starting the application.

    This function checks for the presence of Python, creates a virtual environment, installs dependencies,
    and starts the main application.


    Raises:
        EnvironmentError: If there is an issue with the environment setup or package installation.
    """

    check_python()
    create_venv()
    install_dependencies()
    start_main()

if __name__ == "__main__":
    main()
