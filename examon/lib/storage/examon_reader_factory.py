from .read.fetch import Fetch
from .drivers.content.sqlite3.sqlite3_fetcher import Sqlite3Fetcher
from .drivers.files.local_filesystem_loader import LocalFileSystemLoader

from examon_core.examon_item_registry import ExamonItemRegistry, ItemRegistryFilter


class InMemoryLoader:
    def __init__(self, models):
        self.models = models

    def load(self):
        return self.models


class ExamonReaderFactory:

    @staticmethod
    def load(examon_config, content_mode='sqlite3', file_mode='memory',
             examon_filter=ItemRegistryFilter()):
        record_driver = None
        if content_mode == 'sqlite3':
            record_driver = Sqlite3Fetcher(
                db_file=examon_config.sqlite3_full_path()
            )
        elif file_mode == 'memory':
            record_driver = InMemoryLoader(ExamonItemRegistry.registry())

        blob_driver = LocalFileSystemLoader(examon_config.code_files_full_path())
        fetch = Fetch(record_driver, blob_driver)
        return fetch.load(examon_filter)
