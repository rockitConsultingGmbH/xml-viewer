import subprocess
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def build_executable(script_name, name="app", console=True, add_data=None, icon_path=None):

    command = [
        "pyinstaller",
        "--onefile",
        "--name", name,
        "--hidden-import=lxml",
        "--hidden-import=lxml.etree",
        "--hidden-import=lxml.objectify",
        "--hidden-import=PyQt5",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        script_name
    ]

    if not console:
        command.append("--noconsole")
    if icon_path:
        command.extend(["--icon", icon_path])

    if add_data:
        for source, destination in add_data:
            # Adjust syntax based on the operating system
            formatted_data = f"{source};{destination}" if sys.platform == "win32" else f"{source}:{destination}"
            command.extend(["--add-data", formatted_data])

    logging.info(f"Building executable {name} for {script_name}...")
    try:
        subprocess.run(command, check=True)
        logging.info("Build complete.")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while building the executable: {e}")
        return

    dist_path = os.path.join("dist", os.path.splitext(name)[0] + ".exe")
    if os.path.exists(dist_path):
        logging.info(f"Executable created successfully at: {dist_path}")
    else:
        logging.error("Something went wrong. Executable not found in 'dist' folder.")

if __name__ == "__main__":
    script_name = "app.py"
    executable_name  = "acsftconfig_editor"
    console = True

    add_data = [
        ("database/database.db", "database"),
        ("gui/icon/folder.svg", "gui/icon"),
        ("gui/icon/pick_file.svg", "gui/icon"),
        ("css/right_widget_styling.qss", "css"),
        ("css/tree_widget_styling.qss", "css"),
        ("config.properties", "."),
    ]

    # Optional icon path
    icon_path = None

    build_executable(script_name, name=executable_name , console=False, add_data=add_data, icon_path=icon_path)
