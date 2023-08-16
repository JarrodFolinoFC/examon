from examon.lib.stats import Stats
from examon.lib.package_manager import PackageManager
from examon_core.examon_item_registry import ExamonItemRegistry

from examon.lib.pip_installer import PipInstaller


class OverviewCli:
    @staticmethod
    def process_command():
        package_manager = PackageManager()
        package_manager.load()
        PipInstaller.install(package_manager.packages)
        PipInstaller.import_packages(package_manager.active_packages)
        print('overview')
        print(Stats.calc_stats(ExamonItemRegistry.registry()))
