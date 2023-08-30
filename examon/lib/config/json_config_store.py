import os.path
import os
import json
import logging
from .settings_manager import SettingsManager


class JsonConfigStore:
    DEFAULT_MODULE = 'examon_beginners_package'

    @staticmethod
    def persist(package_manager, full_file_path: str) -> None:
        f = open(full_file_path, "w")
        json_object = json.dumps(package_manager.as_dict(), indent=4)
        f.write(json_object)
        f.close()
        logging.info(f'config saved to {full_file_path}')

    @staticmethod
    def persist_default_config(full_file_path: str) -> None:
        package_manager = SettingsManager()

        package_manager.mode = 'sqlite3'
        package_manager.packages = [
            {
                'name': JsonConfigStore.DEFAULT_MODULE
            }]
        package_manager.active_packages = [JsonConfigStore.DEFAULT_MODULE]

        if not os.path.isfile(full_file_path):
            JsonConfigStore.persist(package_manager, full_file_path)
