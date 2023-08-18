from .sqlite3_driver import Sqlite3Driver
from .local_file_system_driver import LocalFileSystemDriver
from .ingest import Ingest
from .filename_strategy import SimpleFilenameStrategy
from examon_core.examon_item_registry import ExamonItemRegistry


class IngestFactory:
    @staticmethod
    def build(base_dir, test_db_name):
        filename_strategy = SimpleFilenameStrategy(base_dir)
        return Ingest(
            Sqlite3Driver(
                db_file=test_db_name,
                models=ExamonItemRegistry.registry(),
                filename_strategy=filename_strategy
            ),
            LocalFileSystemDriver(
                models=ExamonItemRegistry.registry(),
                filename_strategy=filename_strategy
            )
        )
