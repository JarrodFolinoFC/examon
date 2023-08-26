import os.path
import os
import json
import logging
from ..package_manager import PackageManager


class ExamonConfigJsonInit:
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
        if os.path.isfile(full_file_path):
            print(f'{full_file_path} already exists')
            return

        package_manager = PackageManager()
        dirname = os.path.dirname(full_file_path)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        package_manager.mode = 'sqlite3'
        package_manager.packages = [
            {
                'name': ExamonConfigJsonInit.DEFAULT_MODULE
            }]
        package_manager.active_packages = [ExamonConfigJsonInit.DEFAULT_MODULE]

        if not os.path.isfile(full_file_path):
            ExamonConfigJsonInit.persist(package_manager, full_file_path)
