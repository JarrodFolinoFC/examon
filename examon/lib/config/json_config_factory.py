import os

from .config_structure import ExamonConfigStructure
from .json_config_store import JsonConfigStore
from examon.lib.config.settings_manager_factory import SettingsManagerFactory
from examon.lib.pip_installer import PipInstaller


class JsonConfigFactory:

    @staticmethod
    def install_packages(examon_config):
        path = examon_config.config_full_file_path()
        manager = SettingsManagerFactory.build(path)
        PipInstaller.install(manager.packages)
        PipInstaller.import_packages(manager.active_packages)
        return manager
