from pathlib import Path
import os
import shutil
from sqlalchemy import create_engine

from .drivers.content.sqlite3.sqlite3_writer import Sqlite3Writer
from .drivers.files.local_file_system_writer import LocalFileSystemDriver
from .write.ingest import Writer
from .drivers.files.naming_strategies.filename_strategy import SimpleFilenameStrategy
from .drivers.content.sql_db import QuestionQuery


class ExamonWriterFactory:
    @staticmethod
    def build(base_dir, db_name, models):
        if not os.path.isfile(base_dir):
            Path(base_dir).mkdir(parents=True, exist_ok=True)

        if not os.path.isfile(db_name):
            root_dir = os.path.abspath(os.curdir)
            shutil.copyfile(f'{root_dir}/resources/examon.db', db_name)

        engine = create_engine(f"sqlite+pysqlite:///{db_name}", echo=True)

        ids = QuestionQuery(engine).question_unique_ids()
        models = [model for model in models if model.unique_id not in ids]

        filename_strategy = SimpleFilenameStrategy(base_dir)
        return Writer(
            Sqlite3Writer(
                engine=engine,
                models=models,
                filename_strategy=filename_strategy
            ),
            LocalFileSystemDriver(
                models=models,
                filename_strategy=filename_strategy
            )
        )
