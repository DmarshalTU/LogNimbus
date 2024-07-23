import yaml

class Config:
    def __init__(self, config_file=None):
        self.config = {}
        if config_file:
            self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
        except KeyError:
            return default
        return value
