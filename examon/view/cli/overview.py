from examon.lib.reporting.stats import Stats
from examon.lib.config import SettingsManagerFactory, ConfigStructureFactory
from examon.lib.pip_installer import PipInstaller
from examon.lib.storage.question_factory import QuestionFactory
from .validate_config import ValidateConfig


class OverviewCli:
    @staticmethod
    def process_command():
        config = ConfigStructureFactory.default_config()
        ValidateConfig.config_dir_exists(config)

        PipInstaller.install(config)
        SettingsManagerFactory.build(config.config_full_file_path())
        print('overview')
        manager = SettingsManagerFactory.build(config.config_full_file_path())
        questions = QuestionFactory.load(manager.mode, config)

        print(Stats.calc_stats(questions))
