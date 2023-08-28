from examon.lib.reporting.stats import Stats
from examon.lib.config.settings_manager_factory import SettingsManagerFactory
from examon.lib.config.json_config_factory import JsonConfigFactory
from examon.lib.config.config_structure_factory import ConfigStructureFactory

from examon.lib.storage.question_factory import QuestionFactory


class OverviewCli:
    @staticmethod
    def process_command():
        examon_config = ConfigStructureFactory.init_everything()
        JsonConfigFactory.install_packages(examon_config)
        SettingsManagerFactory.build(examon_config.config_full_file_path())
        print('overview')
        manager = SettingsManagerFactory.build(examon_config.config_full_file_path())
        questions = QuestionFactory.load(manager.mode, examon_config)

        print(Stats.calc_stats(questions))
