import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if it is not already installed."""
    try:
        import PyInstaller  # Try importing PyInstaller
        print("PyInstaller is already installed.")
    except ImportError:
        print("PyInstaller not found. Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable(script_name, icon_path=None, console=True):
    """
    Build an executable from a Python script using PyInstaller.
    
    :param script_name: Name of the Python script to turn into an executable
    :param icon_path: Path to the .ico file to use as the icon (optional)
    :param console: Boolean, if False hides the console window (for GUI apps)
    """
    # PyInstaller command with necessary hidden-imports for lxml and its submodules
    command = [
        "pyinstaller", 
        "--onefile", 
        "--hidden-import=PyQt5", 
        "--hidden-import=lxml", 
        "--hidden-import=lxml.etree", 
        "--hidden-import=lxml.objectify", 
        script_name
    ]

    # Add icon if provided
    if icon_path:
        command.extend(["--icon", icon_path])

    # Hide console window if not desired
    if not console:
        command.append("--noconsole")

    # Run PyInstaller with the specified options
    print(f"Building executable for {script_name}...")
    subprocess.run(command, check=True)
    print("Build complete.")

    # Path to the built executable
    dist_path = os.path.join("dist", os.path.splitext(script_name)[0] + ".exe")
    if os.path.exists(dist_path):
        print(f"Executable created successfully at: {dist_path}")
    else:
        print("Something went wrong. Executable not found in 'dist' folder.")

if __name__ == "__main__":
    # Specify the name of your Python script here
    script_name = "app.py"  # Replace with your actual script name
    icon_path = "your_icon.ico"  # Replace with the path to your icon file if needed, or None
    console = True  # Set to False if you don't want a console window for GUI apps

    install_pyinstaller()  # Ensure PyInstaller is installed
    #build_executable(script_name, icon_path=icon_path, console=console)  # Build the executable
    build_executable(script_name)  # Build the executable

