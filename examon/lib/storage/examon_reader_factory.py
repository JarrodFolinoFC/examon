from .read.fetch import Reader
from .drivers.content.sqlite3.sqlite3_reader import Sqlite3Reader
from .drivers.content.in_memory.in_memory import InMemoryReader
from .drivers.files import LocalFileSystemReader
from ..config import ExamonConfigDir
from examon_core.examon_item_registry import ExamonItemRegistry, ItemRegistryFilter


class ExamonReaderFactory:

    @staticmethod
    def load(examon_config_dir: ExamonConfigDir,
             content_mode: str = 'sqlite3',
             examon_filter: ItemRegistryFilter = ItemRegistryFilter()) -> list:
        content_reader_driver = ExamonReaderFactory.get_content_driver(content_mode, examon_config_dir)

        file_reader_driver = LocalFileSystemReader()
        reader = Reader(content_reader_driver, file_reader_driver)
        return reader.load(examon_filter)

    @staticmethod
    def get_content_driver(content_mode, examon_config_dir):
        if content_mode == 'sqlite3':
            return Sqlite3Reader(
                db_file=examon_config_dir.sqlite3_full_path()
            )
        elif content_mode == 'memory':
            return InMemoryReader(ExamonItemRegistry.registry())
