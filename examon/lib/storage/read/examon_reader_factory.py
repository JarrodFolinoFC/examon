from .reader import Reader
from .content.sqlite3.sqlite3_reader import Sqlite3Reader
from .content.in_memory.in_memory import InMemoryReader
from .files.local_file_system_reader import LocalFileSystemReader

from ...config import ExamonConfigDir
from examon_core.examon_item_registry import ExamonItemRegistry, ItemRegistryFilter


class ExamonReaderFactory:

    @staticmethod
    def load(examon_config_dir: ExamonConfigDir,
             content_mode: str = 'sqlite3',
             file_mode: str = 'memory',
             examon_filter: ItemRegistryFilter = ItemRegistryFilter()) -> list:
        content_reader_driver = None
        if content_mode == 'sqlite3':
            content_reader_driver = Sqlite3Reader(
                db_file=examon_config_dir.sqlite3_full_path()
            )
        elif file_mode == 'memory':
            content_reader_driver = InMemoryReader(ExamonItemRegistry.registry())

        file_reader_driver = LocalFileSystemReader()
        reader = Reader(content_reader_driver, file_reader_driver)
        return reader.load(examon_filter)
