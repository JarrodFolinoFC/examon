import os.path
import os

DEFAULT_FOLDER = '~/.examon'


class ExamonConfig:
    def __init__(self, settings_file='config.json'):
        self.settings_file = settings_file
        self.examon_dir = os.path.expanduser(DEFAULT_FOLDER)

    def full_file_path(self):
        return f'{self.examon_dir}/{self.settings_file}'

    @staticmethod
    def create_config_folder():
        examon_dir = os.path.expanduser(DEFAULT_FOLDER)
        is_exist = os.path.exists(examon_dir)
        if not is_exist:
            os.makedirs(examon_dir)
