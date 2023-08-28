from examon.lib.reporting.stats import Stats
from examon.lib.config.settings_manager_factory import SettingsManagerFactory
from examon.lib.config.json_config_factory import JsonConfigFactory

from examon.lib.storage.question_factory import QuestionFactory

from examon.lib.config.config_structure_factory import ConfigStructureFactory
from .validate_config import ValidateConfig


class OverviewCli:
    @staticmethod
    def process_command():
        config = ConfigStructureFactory.default_config()
        ValidateConfig.config_dir_exists(config)

        JsonConfigFactory.install_packages(config)
        SettingsManagerFactory.build(config.config_full_file_path())
        print('overview')
        manager = SettingsManagerFactory.build(config.config_full_file_path())
        questions = QuestionFactory.load(manager.mode, config)

        print(Stats.calc_stats(questions))
