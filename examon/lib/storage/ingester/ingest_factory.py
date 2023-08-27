from pathlib import Path
import os
import shutil
from sqlalchemy import create_engine

from .sqlite3_driver import Sqlite3Driver
from .local_file_system_driver import LocalFileSystemDriver
from .ingest import Ingest
from .filename_strategy import SimpleFilenameStrategy
from .question_queries import QuestionQueries


class IngestFactory:
    @staticmethod
    def build(base_dir, db_name, models):
        if not os.path.isfile(base_dir):
            Path(base_dir).mkdir(parents=True, exist_ok=True)

        if not os.path.isfile(db_name):
            root_dir = os.path.abspath(os.curdir)
            shutil.copyfile(f'{root_dir}/resources/examon.db', db_name)

        engine = create_engine(f"sqlite+pysqlite:///{db_name}", echo=True)

        ids = QuestionQueries(engine).question_unique_ids()
        models = [model for model in models if model.unique_id not in ids]

        filename_strategy = SimpleFilenameStrategy(base_dir)
        return Ingest(
            Sqlite3Driver(
                engine=engine,
                models=models,
                filename_strategy=filename_strategy
            ),
            LocalFileSystemDriver(
                models=models,
                filename_strategy=filename_strategy
            )
        )
