import json
import os

class SettingsManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.settings = {}
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            except (json.JSONDecodeError, Exception) as e:
                print(f"Warning: Error loading {self.config_file}: {e}. Using defaults.")
                self._set_defaults()
        else:
            self._set_defaults()
            self.save_settings()

    def _set_defaults(self):
        self.settings = {
            'last_opened_dir': os.path.expanduser("~"),
            'last_saved_report_dir': os.path.expanduser("~"),
            'last_saved_plot_dir': os.path.expanduser("~")
        }

    def get_setting(self, key, default_value=None):
        return self.settings.get(key, default_value)

    def set_setting(self, key, value):
        self.settings[key] = value

    def save_settings(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error: Could not save settings to {self.config_file}: {e}")
