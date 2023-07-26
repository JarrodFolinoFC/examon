import os.path
import os
import json
import logging

from examon.lib.examon_config import ExamonConfig


class PackageManager:
    DEFAULT_MODULE = 'examon_beginners_package'

    def __init__(self, settings_file='.examon'):
        self.packages = []
        self.active_packages = []
        self.settings_file = settings_file
        self.full_file_path = ExamonConfig().full_file_path()

    def reset(self):
        self.packages = []
        self.active_packages = []

    def add(self, package, url=None):
        if package is None or package == '':
            logging.debug('Cannot add package not specified')
            return

        data = {'name': package}
        if url:
            data |= {'url': url}
        if package not in self.packages:
            self.packages.append(data)

    def add_active(self, package):
        if package not in self.active_packages:
            self.active_packages.append(package)

    def remove(self, package):
        index = next(
            (index for (
                index,
                d) in enumerate(
                self.packages) if d["name"] == package),
            None)
        logging.debug(f'Removing package {package}')
        if index is not None:
            del self.packages[index]

    def remove_active(self, package):
        if package in self.active_packages:
            self.active_packages.remove(package)

    def as_dict(self):
        return {
            'packages':
                {
                    'all': self.packages,
                    'active': self.active_packages
                }
        }

    def load(self):
        with open(self.full_file_path, 'r') as f:
            data = json.load(f)

        self.packages = data['packages']['all']
        self.active_packages = data['packages']['active']

    def persist(self):
        f = open(self.full_file_path, "w")
        json_object = json.dumps(self.as_dict(), indent=4)
        f.write(json_object)
        f.close()
        logging.info(f'config saved to {self.full_file_path}')

    def persist_default_config(self):
        self.packages = [
            {
                'name': PackageManager.DEFAULT_MODULE
            }]
        ExamonConfig.create_config_folder()
        self.active_packages = [PackageManager.DEFAULT_MODULE]

        if not os.path.isfile(self.full_file_path):
            self.persist()
