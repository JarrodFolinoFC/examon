import pytest

from examon.lib.storage.read_write.sql_db import QuestionQuery

from helpers import Helpers
from fixtures_loader import FixturesLoader


@pytest.fixture(autouse=True)
def run_around_tests():
    Helpers.clean()
    yield
    Helpers.clean()


class TestQuestionQuery:
    def test_qq(self):
        engine = Helpers.setup_everything2(FixturesLoader.load_all)
        assert QuestionQuery(engine).question_unique_ids() == [
            '94906873137099624396142246939254', '24260242706113154843827424114127'
        ]
