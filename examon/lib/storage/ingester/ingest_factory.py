from pathlib import Path
import os
import shutil

from .sqlite3_driver import Sqlite3Driver
from .local_file_system_driver import LocalFileSystemDriver
from .ingest import Ingest
from .filename_strategy import SimpleFilenameStrategy


class IngestFactory:
    @staticmethod
    def build(base_dir, db_name, models):
        if not os.path.isfile(base_dir):
            Path(base_dir).mkdir(parents=True, exist_ok=True)

        if not os.path.isfile(db_name):
            root_dir = os.path.abspath(os.curdir)
            shutil.copyfile(f'{root_dir}/resources/examon.db', db_name)

        filename_strategy = SimpleFilenameStrategy(base_dir)
        return Ingest(
            Sqlite3Driver(
                db_file=db_name,
                models=models,
                filename_strategy=filename_strategy
            ),
            LocalFileSystemDriver(
                models=models,
                filename_strategy=filename_strategy
            )
        )
