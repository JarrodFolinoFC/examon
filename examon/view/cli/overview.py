from examon.lib.stats import Stats
from examon_core.examon_item_registry import ExamonItemRegistry
from examon.lib.settings_manager_factory import SettingsManagerFactory
from examon.lib.config.examon_config import ExamonConfig

from examon.lib.pip_installer import PipInstaller
from examon.lib.storage.question_factory import QuestionFactory


class OverviewCli:
    @staticmethod
    def process_command():
        examon_config = ExamonConfig()
        package_manager = SettingsManagerFactory.build(examon_config.config_full_file_path())
        PipInstaller.install(package_manager.packages)
        PipInstaller.import_packages(package_manager.active_packages)
        print('overview')
        examon_config = ExamonConfig()
        manager = SettingsManagerFactory.build(examon_config.config_full_file_path())
        questions = QuestionFactory.load(manager.mode, examon_config)

        print(Stats.calc_stats(questions))
