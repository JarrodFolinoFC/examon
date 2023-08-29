from .read.fetch import Reader
from .drivers.content.sqlite3.sqlite3_reader import Sqlite3Reader
from .drivers.files.local_filesystem_reader import LocalFileSystemReader

from examon_core.examon_item_registry import ExamonItemRegistry, ItemRegistryFilter


class InMemoryLoader:
    def __init__(self, models):
        self.models = models

    def load(self):
        return self.models


class ExamonReaderFactory:

    @staticmethod
    def load(examon_config_dir, content_mode='sqlite3', file_mode='memory',
             examon_filter=ItemRegistryFilter()):
        record_driver = None
        if content_mode == 'sqlite3':
            record_driver = Sqlite3Reader(
                db_file=examon_config_dir.sqlite3_full_path()
            )
        elif file_mode == 'memory':
            record_driver = InMemoryLoader(ExamonItemRegistry.registry())

        blob_driver = LocalFileSystemReader(examon_config_dir.code_files_full_path())
        fetch = Reader(record_driver, blob_driver)
        return fetch.load(examon_filter)
