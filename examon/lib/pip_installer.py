import subprocess
import sys
import importlib.util
import logging

from examon.lib.config.settings_manager_factory import SettingsManagerFactory


class PipInstaller:

    @staticmethod
    def install(examon_config):
        path = examon_config.config_full_file_path()
        manager = SettingsManagerFactory.build(path)
        logging.info(f"installing {len(manager.packages)} repos")
        for package in manager.packages:
            with open('pip_install.log', "w") as outfile:
                cmd = [sys.executable, "-m", "pip", "install", package['name'], '--upgrade']
                logging.debug(cmd)
                subprocess.run(cmd, stdout=outfile)
        PipInstaller.import_packages(manager.active_packages)
        return manager

    @staticmethod
    def is_package_installed(package):
        if importlib.util.find_spec(package) is None:
            return False
        return True

    @staticmethod
    def import_packages(packages):
        logging.info(f'Importing Packages ({len(packages)})')
        for repo in packages:
            __import__(repo, fromlist=['*'])
