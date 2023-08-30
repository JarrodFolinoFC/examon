import json
from .settings_manager import SettingsManager


class SettingsManagerFactory:
    @staticmethod
    def build(full_file_path: str) -> SettingsManager:
        with open(full_file_path, 'r') as f:
            data = json.load(f)
        package_manager = SettingsManager()
        package_manager.packages = data['packages']['all']
        package_manager.active_packages = data['packages']['active']
        package_manager.mode = data['mode']

        return package_manager
