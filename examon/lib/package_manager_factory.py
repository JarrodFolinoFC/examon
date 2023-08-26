import json
from .package_manager import PackageManager


class PackageManagerFactory:
    @staticmethod
    def build(full_file_path):
        with open(full_file_path, 'r') as f:
            data = json.load(f)
        package_manager = PackageManager()
        package_manager.packages = data['packages']['all']
        package_manager.active_packages = data['packages']['active']
        package_manager.mode = data['mode']

        return package_manager
