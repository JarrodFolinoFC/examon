from examon.lib.reporting.stats import Stats
from examon.lib.config import SettingsManagerFactory, ConfigDirFactory
from examon.lib.pip_installer import PipInstaller
from examon.lib.storage.read.examon_reader_factory import ExamonReaderFactory
from .validate_config import ValidateConfig


class OverviewCli:
    @staticmethod
    def process_command():
        config = ConfigDirFactory.build()
        ValidateConfig.config_dir_exists(config)

        PipInstaller.install(config)
        SettingsManagerFactory.build(config.config_full_file_path())
        print('overview')
        questions = ExamonReaderFactory.load(config)
        print(Stats.calc_stats(questions))
