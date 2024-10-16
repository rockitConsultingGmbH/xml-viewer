class ConfigManager:
    def __init__(self):
        self.config_id = None
        self.config_filename = None
        self.config_filepath = None
config_manager = ConfigManager()

#class ConfigManager:
#    _instance = None
#
#    def __init__(self):
#        self.config_id = None
#        self.config_filename = None
#        self.config_filepath = None
#
#    @classmethod
#    def get_instance(cls):
#        if cls._instance is None:
#            cls._instance = cls()
#        return cls._instance
#
## Accessing the singleton instance
#config_manager = ConfigManager.get_instance()

