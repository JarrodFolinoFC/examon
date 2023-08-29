import os.path
import os

DEFAULT_FOLDER = '~/.examon'


class ExamonConfigDir:
    def __init__(self, settings_file=None, sqlite3_db_file=None,
                 files_dir=None, results_dir=None):
        self.settings_file = settings_file
        self.sqlite3_db_file = sqlite3_db_file
        self.files_dir = files_dir
        self.results_dir = results_dir
        self.examon_dir = os.path.expanduser(DEFAULT_FOLDER)

    def sqlite3_full_path(self):
        return f'{self.examon_dir}/{self.sqlite3_db_file}'

    def config_full_file_path(self):
        return f'{self.examon_dir}/{self.settings_file}'

    def code_files_full_path(self):
        return f'{self.examon_dir}/{self.files_dir}'

    def results_full_path(self):
        return f'{self.examon_dir}/{self.results_dir}'
