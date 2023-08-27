import pytest
from sqlalchemy.orm import Session
from examon_core.examon_item_registry import ExamonItemRegistry
from examon_core.examon_item import examon_item

from examon.lib.utils.sql_alchemy_ext import SqlAlchemyExtension

from helpers import Helpers


def load_question():
    @examon_item(tags=['a_tag'])
    def question_1():
        return 1


@pytest.fixture(autouse=True)
def run_around_tests():
    ExamonItemRegistry.reset()
    yield
    ExamonItemRegistry.reset()
    Helpers.clean()


class TestResultManager:
    def test_creates_valid_json(self):
        pass
        # with Session(Helpers.setup_everything(load_question(), 1)[1]
        #              ) as session:
        #     SqlAlchemyExtension.get_or_create(session)

