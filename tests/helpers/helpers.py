import shutil
import uuid
import os
from examon.lib.ingester.ingest_factory import IngestFactory
from examon_core.examon_item_registry import ExamonItemRegistry


class Helpers:
    @staticmethod
    def test_db(current_working_directory):
        src_file = f'{current_working_directory}/tests/empty.test.db'
        destination = f'{current_working_directory}/tests/tmp/db/test.{uuid.uuid4()}.db'
        shutil.copy(src_file, destination)
        return destination

    @staticmethod
    def run_ingester(f):
        f()
        cwd = os.getcwd()
        test_db_name = Helpers.test_db(cwd)
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
