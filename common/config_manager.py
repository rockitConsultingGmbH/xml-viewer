class ConfigManager:
    def __init__(self):
        self.config_id = None
        self.config_filename = None
        self.config_filepath = None
config_manager = ConfigManager()

#class ConfigManager:
#    _instance = None
#
#    def __new__(cls, *args, **kwargs):
#        if not cls._instance:
#            cls._instance = super(ConfigManager, cls).__new__(cls, *args, **kwargs)
#        return cls._instance
#
#    def __init__(self):
#        if not hasattr(self, '_initialized'):  # Prevent reinitialization
#            self._config_id = None
#            self._config_filename = None
#            self._config_filepath = None
#            self._initialized = True
#
#    @classmethod
#    def get_instance(cls):
#        if not cls._instance:
#            cls._instance = cls()
#        return cls._instance
#
#    @property
#    def config_id(self):
#        return self._config_id
#
#    @config_id.setter
#    def config_id(self, value):
#        self._config_id = value
#
#    @property
#    def config_filename(self):
#        return self._config_filename
#
#    @config_filename.setter
#    def config_filename(self, value):
#        self._config_filename = value
#
#    @property
#    def config_filepath(self):
#        return self._config_filepath
#
#    @config_filepath.setter
#    def config_filepath(self, value):
#        self._config_filepath = value

# Usage
#config_manager = ConfigManager.get_instance()

