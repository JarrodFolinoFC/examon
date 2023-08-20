from examon.lib.examon_config import ExamonConfig

import logging


class PackageManager:
    def __init__(self, settings_file='.examon'):
        self.packages = []
        self.active_packages = []
        self.mode = None
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
        self.remove_active(package)

    def remove_active(self, package):
        if package in self.active_packages:
            self.active_packages.remove(package)

    def as_dict(self):
        return {
            'mode': self.mode,
            'packages':
                {
                    'all': self.packages,
                    'active': self.active_packages
                }
        }
