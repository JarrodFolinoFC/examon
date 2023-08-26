from examon.lib.stats import Stats
from examon_core.examon_item_registry import ExamonItemRegistry
from examon.lib.package_manager_factory import PackageManagerFactory
from examon.lib.config.examon_config import ExamonConfig

from examon.lib.pip_installer import PipInstaller


class OverviewCli:
    @staticmethod
    def process_command():
        examon_config = ExamonConfig()
        package_manager = PackageManagerFactory.build(examon_config.config_full_file_path())
        PipInstaller.install(package_manager.packages)
        PipInstaller.import_packages(package_manager.active_packages)
        print('overview')
        print(Stats.calc_stats(ExamonItemRegistry.registry()))
