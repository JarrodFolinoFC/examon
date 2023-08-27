import pytest

from sqlalchemy.orm import Session

from examon_core.examon_item_registry import ExamonItemRegistry

from examon.lib.storage.ingester.question_queries import QuestionQueries

from helpers import Helpers
from fixtures_loader import FixturesLoader


@pytest.fixture(autouse=True)
def run_around_tests():
    ExamonItemRegistry.reset()
    yield
    ExamonItemRegistry.reset()
    Helpers.clean()


class TestIngest:
    def test_qq(self):
        with Session(Helpers.setup_everything(FixturesLoader.load_q1)[1]) as _:
            pass
        engine = Helpers.setup_everything(FixturesLoader.load_q2)[1]
        assert QuestionQueries(engine).question_unique_ids() == [
            '94906873137099624396142246939254', '24260242706113154843827424114127'
        ]

