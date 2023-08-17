import os

from examon.lib.ingester.ingest import Ingest
from examon.lib.ingester.sqlite3_driver import Sqlite3Driver
from examon_core.examon_item import examon_item
from examon_core.examon_item_registry import ExamonItemRegistry

import pytest


@examon_item(tags=['a'])
def question_1():
    return 1


current_working_directory = os.getcwd()


class TestSqlite3Driver:
    def test_e2e(self):
        ingester = Ingest([], Sqlite3Driver(f'{current_working_directory}/tests/test.db',
                                            ExamonItemRegistry.registry()))
        ingester.run()
