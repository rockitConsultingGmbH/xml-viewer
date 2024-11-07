import subprocess
import sys
import os
import logging

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from common.config_manager import ConfigManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExecutableBuilder:
    def __init__(self, script_name, name="app", console=True, add_data=None, icon_path=None):
        self.script_name = script_name
        self.name = name
        self.console = console
        self.add_data = add_data
        self.icon_path = icon_path

    def build(self):
        command = [
            sys.executable,  # Use Python executable to run PyInstaller
            "-m", "PyInstaller",
            "--onefile",
            "--name", self.name,
            "--hidden-import=lxml",
            "--hidden-import=lxml.etree",
            "--hidden-import=lxml.objectify",
            "--hidden-import=PyQt5",
            "--hidden-import=PyQt5.QtWidgets",
            "--hidden-import=PyQt5.QtCore",
            "--hidden-import=PyQt5.QtGui",
            self.script_name
        ]

        if not self.console:
            command.append("--noconsole")
        if self.icon_path:
            command.extend(["--icon", self.icon_path])

        if self.add_data:
            for source, destination in self.add_data:
                formatted_data = f"{source};{destination}" if sys.platform == "win32" else f"{source}:{destination}"
                command.extend(["--add-data", formatted_data])

        logging.info(f"Building executable {self.name} for {self.script_name}...")
        logging.debug(f"Full command: {' '.join(command)}")

        try:
            subprocess.run(command, check=True)
            logging.info("Build complete.")
            
            # Print the path where the executable is created
            dist_path = os.path.join("dist", self.name + (".exe" if sys.platform == "win32" else ""))
            if os.path.exists(dist_path):
                logging.info(f"Executable created successfully at: {dist_path}")
                print(f"Executable created successfully at: {os.path.abspath(dist_path)}")
            else:
                logging.error("Something went wrong. Executable not found in 'dist' folder.")
        
        except subprocess.CalledProcessError as e:
            logging.error(f"An error occurred while building the executable: {e}")
        except FileNotFoundError as e:
            logging.error(f"FileNotFoundError: {e}")

if __name__ == "__main__":
    script_name = "app.py"
    config_manager = ConfigManager()
    version = config_manager.get_property_from_properties("version")
    app_name = config_manager.get_property_from_properties("appName")
    executable_name = f"{app_name}_{version}".lower()
    console = True

    add_data = [
        ("database/database.db", "database"),
        ("gui/icon/folder.svg", "gui/icon"),
        ("gui/icon/main.svg", "gui/icon"),
        ("gui/icon/pick_file.svg", "gui/icon"),
        ("gui/icon/search.svg", "gui/icon"),
        ("css/right_widget_styling.qss", "css"),
        ("css/tree_widget_styling.qss", "css"),
        ("config.properties", "."),
    ]

    # Optional icon path
    icon_path = None

    builder = ExecutableBuilder(script_name, name=executable_name, console=True, add_data=add_data, icon_path=icon_path)
    builder.build()
