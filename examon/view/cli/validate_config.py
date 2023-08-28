import os
import sys


class ValidateConfig:
    @staticmethod
    def config_dir_exists(config):
        if not os.path.exists(config.examon_dir):
            print('No ~/.examon config directory found. Run `examon init && examon package install`')
            sys.exit(0)
