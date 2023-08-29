import shutil
import uuid
import os
from examon.lib.storage.write.ingest_factory import IngestFactory
from examon_core.examon_item_registry import ExamonItemRegistry
from sqlalchemy import create_engine


class Helpers:
    @staticmethod
    def test_db(current_working_directory):
        src_file = f'{current_working_directory}/resources/examon.db'
        destination = f'{current_working_directory}/tests/tmp/db/test.{uuid.uuid4()}.db'
        shutil.copy(src_file, destination)
        return destination

    @staticmethod
    def run_ingester(f, existing_test_db_name=None):
        f()
        cwd = os.getcwd()
        if existing_test_db_name is None:
            test_db_name = Helpers.test_db(cwd)
        else:
            test_db_name = existing_test_db_name

        IngestFactory.build(f'{cwd}/tests/tmp/files', test_db_name,
                            ExamonItemRegistry.registry()).run()
        return test_db_name

    @staticmethod
    def clean():
        cwd = os.getcwd()
        for file in os.scandir(f'{cwd}/tests/tmp/db'):
            if file.name.endswith(".db"):
                os.unlink(file.path)
        for directory in os.scandir(f'{cwd}/tests/tmp/files'):
            if os.path.isdir(directory):
                shutil.rmtree(directory)
        ExamonItemRegistry.reset()

    @staticmethod
    def setup_everything(f, existing_test_db_name=None):
        test_db_name = Helpers.run_ingester(f, existing_test_db_name=existing_test_db_name)
        return test_db_name, create_engine(f"sqlite+pysqlite:///{test_db_name}", echo=True)
