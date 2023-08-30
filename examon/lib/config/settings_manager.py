import logging


class SettingsManager:
    def __init__(self):
        self.packages = []
        self.active_packages = []
        self.mode = None

    def reset(self):
        self.packages = []
        self.active_packages = []

    def add(self, package_name: str, url: str = None) -> None:
        if package_name is None or package_name == '':
            logging.debug('Cannot add package not specified')
            return

        data = {'name': package_name}
        if url:
            data |= {'url': url}

        if package_name not in [package['name'] for package in self.packages]:
            self.packages.append(data)

    def add_active(self, package: str):
        if package not in self.active_packages:
            self.active_packages.append(package)

    def remove(self, package: str) -> None:
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

    def remove_active(self, package: str):
        if package in self.active_packages:
            self.active_packages.remove(package)

    def as_dict(self) -> dict:
        return {
            'mode': self.mode,
            'packages':
                {
                    'all': self.packages,
                    'active': self.active_packages
                }
        }
