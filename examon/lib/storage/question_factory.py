from examon.lib.storage.fetcher.fetch import Fetch
from examon.lib.storage.fetcher.sqlite3_fetcher import Sqlite3Fetcher

from examon_core.examon_item_registry import ExamonItemRegistry, ItemRegistryFilter


class QuestionFactory:
    @staticmethod
    def load(mode, examon_config, examon_filter=ItemRegistryFilter()):
        if mode == 'sqlite3':
            return QuestionFactory.load_from_db(examon_config, examon_filter)
        elif mode == 'memory':
            return ExamonItemRegistry.registry(examon_filter)

    @staticmethod
    def load_from_db(examon_config, examon_filter):
        class FileLoader:
            def __init__(self, models):
                self.models = models

            def load(self):
                for model in self.models:
                    with open(self.path, "r") as f:
                        model.function_src = f.read()

        record_driver = Sqlite3Fetcher(
            db_file=examon_config.sqlite3_full_path()
        )
        blob_driver = FileLoader
        fetch = Fetch(record_driver, blob_driver)
        return fetch.load(examon_filter)
