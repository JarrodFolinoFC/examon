import os.path
import os
import json
import subprocess
import sys
import importlib.util


class PackageManager:
    DEFAULT_MODULE = 'examon_repo_1'
    DEFAULT_PIP = 'https://test.pypi.org/simple/'

    def __init__(self, settings_file='.examon'):
        self.packages = []
        self.active_packages = []
        self.settings_file = settings_file

    def install(self):
        print(f"installing {len(self.packages)} repos")
        for package in self.packages:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package['name'], '--upgrade'])

    def reset(self):
        self.packages = []
        self.active_packages = []

    def add(self, package, url=None):
        if package is None or package == '':
            return

        data = {'name': package}
        if url:
            data |= {'url': url}
        self.packages.append(data)

    def remove(self, package):
        index = next(
            (index for (
                index,
                d) in enumerate(
                self.packages) if d["name"] == package),
            None)
        del self.packages[index]

    def add_active(self, package):
        if package not in self.active_packages:
            self.active_packages.append(package)

    def remove_active(self, package):
        self.active_packages.remove(package)

    def import_packages(self):
        print(f'Importing Packages ({len(self.active_packages)})')
        for repo in self.active_packages:
            __import__(repo, fromlist=['*'])


    def as_dict(self):
        return {
            'packages':
                {
                    'all': self.packages,
                    'active': self.active_packages
                }
        }

    def persist(self):
        f = open(self.full_file_path(), "w")
        json_object = json.dumps(self.as_dict(), indent=4)
        f.write(json_object)
        f.close()

    def load(self):
        with open(self.full_file_path(), 'r') as f:
            data = json.load(f)

        self.packages = data['packages']['all']
        self.active_packages = data['packages']['active']

    def full_file_path(self):
        home_directory = os.path.expanduser('~')
        file = f'{home_directory}/{self.settings_file}'
        return file

    def persist_default_config(self):
        self.packages = [
            {
                'name': PackageManager.DEFAULT_MODULE,
                'pip_url': PackageManager.DEFAULT_PIP
            }]
        self.active_packages = [PackageManager.DEFAULT_MODULE]
        if not os.path.isfile(self.full_file_path()):
            self.persist()


    @staticmethod
    def is_package_installed(package_name):
        if importlib.util.find_spec(package_name) is None:
            return False
        return True

