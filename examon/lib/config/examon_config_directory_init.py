import os
import shutil


class ExamonConfigDirectoryInit:

    @staticmethod
    def init_everything(examon_config):

        db_full_file_path = examon_config.sqlite3_full_path()
        dirname = os.path.dirname(db_full_file_path)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        if not os.path.exists(examon_config.results_full_path()):
            os.mkdir(examon_config.results_full_path())

        if not os.path.isfile(db_full_file_path):
            from pathlib import Path

            current_dir = Path(__file__)
            examon_dir = [p for p in current_dir.parents if p.parts[-1] == 'examon'][0]
            shutil.copy(f'{examon_dir}/../resources/examon.db', db_full_file_path)
