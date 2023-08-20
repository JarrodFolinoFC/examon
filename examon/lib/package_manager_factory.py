import os.path
import os
import json
import logging
from .package_manager import PackageManager


class PackageManagerFactory:
    DEFAULT_MODULE = 'examon_beginners_package'

    @staticmethod
    def persist(package_manager, full_file_path):
        f = open(full_file_path, "w")
        json_object = json.dumps(package_manager.as_dict(), indent=4)
        f.write(json_object)
        f.close()
        logging.info(f'config saved to {full_file_path}')

    @staticmethod
    def persist_default_config(full_file_path):
        package_manager = PackageManager()
        package_manager.mode = 'sqlite3'
        package_manager.packages = [
            {
                'name': PackageManagerFactory.DEFAULT_MODULE
            }]
        package_manager.active_packages = [PackageManagerFactory.DEFAULT_MODULE]

        if not os.path.isfile(full_file_path):
            PackageManagerFactory.persist(package_manager)

    @staticmethod
    def load(full_file_path):
        with open(full_file_path, 'r') as f:
            data = json.load(f)
        package_manager = PackageManager()
        package_manager.packages = data['packages']['all']
        package_manager.active_packages = data['packages']['active']

        return package_manager
