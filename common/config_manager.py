import os
import sys

class ConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.config_id = None
            self.config_filename = "config.properties"
            self.config_filepath = self.get_config_filepath()
            self.initialized = True

    def get_config_filepath(self):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        return os.path.join(base_path, self.config_filename)

    def get_property_from_properties(self, property_name):
        value = "Unknown"
        try:
            with open(self.config_filepath, "r") as file:
                for line in file:
                    line = line.strip()
                    if line.startswith(f"{property_name}="):
                        value = line.split("=", 1)[1].strip()
                        break
        except Exception as e:
            print(f"Error reading {property_name} from properties file: {e}")
        return value
