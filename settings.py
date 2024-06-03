import json


class Settings:

    def __init__(self, settings_name, default_settings={}):
        self.settings_file_name = settings_name + ".json"
        if self.get_settings() is None:
            self.save_settings(default_settings)

    def get_settings(self):
        try:
            with open(self.settings_file_name) as f:
                return json.load(f)
        except OSError:
            return None

    def get(self, key):
        return self.get_settings().get(key, None)

    def save_settings(self, settings):
        with open(self.settings_file_name, "w") as f:
            json.dump(settings, f)
