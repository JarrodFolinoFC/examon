import os
import shutil
from .json_config_store import JsonConfigStore
from .config_dir import ExamonConfigDir


class ConfigDirFactory:

    @staticmethod
    def init_everything():
        examon_config_dir = ConfigDirFactory.default_config()

        db_full_file_path = examon_config_dir.sqlite3_full_path()

        dirname = os.path.dirname(db_full_file_path)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        dirname = os.path.dirname(examon_config_dir.config_full_file_path())
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        if not os.path.exists(examon_config_dir.results_full_path()):
            os.mkdir(examon_config_dir.results_full_path())

        if not os.path.isfile(db_full_file_path):
            from pathlib import Path

            current_dir = Path(__file__)
            examon_dir = [p for p in current_dir.parents if p.parts[-1] == 'examon'][0]
            shutil.copy(f'{examon_dir}/../resources/examon.db', db_full_file_path)

        if os.path.isfile(examon_config_dir.config_full_file_path()):
            print(f'{examon_config_dir.config_full_file_path()} already exists')
        else:
            JsonConfigStore.persist_default_config(examon_config_dir.config_full_file_path())

        return examon_config_dir

    @staticmethod
    def default_config():
        return ExamonConfigDir(settings_file='config.json', sqlite3_db_file='examon.db',
                                     files_dir='files', results_dir='results')
