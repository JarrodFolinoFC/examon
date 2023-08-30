import pytest

from examon.lib.storage.read.content.sqlite3.sqlite3_reader import Sqlite3Reader

from examon_core.models.question import BaseQuestion, MultiChoiceQuestion
from examon_core.examon_item_registry import ItemRegistryFilter
from examon_core.models.code_metrics import CodeMetrics
from helpers import Helpers
from fixtures_loader import FixturesLoader


@pytest.fixture(autouse=True)
def run_around_tests():
    Helpers.clean()
    yield
    Helpers.clean()


class TestSqlite3Reader:
    def test_creates_multichoice_record(self):
        engine = Helpers.setup_everything2(FixturesLoader.load_multichoice)
        fetcher = Sqlite3Reader(engine=engine)
        assert len(fetcher.load()) == 1
        q1 = fetcher.load()[0]
        assert q1.__class__ == MultiChoiceQuestion
        assert q1.choices == ['1', '2', '3']

    def test_query_by_filter_tags_any_1(self):
        engine = Helpers.setup_everything2(FixturesLoader.load_questions_with_tags)
        fetcher = Sqlite3Reader(engine=engine)
        results = fetcher.load(ItemRegistryFilter(tags_any=['b_tag', 'not_here']))
        assert len(results) == 2
        for result in results:
            assert 'b_tag' in [tag for tag in result.tags]

    def test_creates_multiple_records(self):
        engine = Helpers.setup_everything2(FixturesLoader.load_all)
        fetcher = Sqlite3Reader(engine=engine)
        assert len(fetcher.load()) == 2
        q1 = fetcher.load()[1]
        assert q1.unique_id == '24260242706113154843827424114127'
        assert q1.internal_id == 'question_two'
        assert q1.__class__ == BaseQuestion
        assert q1.tags == ['a', 'b']
        assert q1.print_logs == ['2']
        assert q1.metrics.__class__ == CodeMetrics
        assert q1.metrics.difficulty == 0.0
        assert q1.metrics.loc == 4

    def test_query_by_filter_tags_any_2(self):
        engine = Helpers.setup_everything2(FixturesLoader.load_questions_with_tags)
        fetcher = Sqlite3Reader(engine=engine)
        results = fetcher.load(ItemRegistryFilter(tags_any=['a_tag', 'not_here', 'not_here_again']))
        assert len(results) == 3
        for result in results:
            assert 'a_tag' in [tag for tag in result.tags]

    def test_query_by_filter_tags_any_3(self):
        engine = Helpers.setup_everything2(FixturesLoader.load_questions_with_tags)
        fetcher = Sqlite3Reader(engine=engine)
        results = fetcher.load(ItemRegistryFilter(tags_any=['c_tag']))
        assert len(results) == 1
        for result in results:
            assert 'c_tag' in [tag for tag in result.tags]

    def test_query_by_filter_tags_any_4(self):
        engine = Helpers.setup_everything2(FixturesLoader.load_questions_with_tags)
        fetcher = Sqlite3Reader(engine=engine)
        results = fetcher.load(ItemRegistryFilter(tags_any=['d_tag']))
        assert len(results) == 0

    def test_query_by_filter_tags_all(self):
        engine = Helpers.setup_everything2(FixturesLoader.load_questions_with_tags)
        fetcher = Sqlite3Reader(engine=engine)
        results = fetcher.load(ItemRegistryFilter(tags_all=['a_tag']))
        assert len(results) == 3

    def test_query_by_filter_tags_all_2(self):
        engine = Helpers.setup_everything2(FixturesLoader.load_questions_with_tags)
        fetcher = Sqlite3Reader(engine=engine)
        results = fetcher.load(ItemRegistryFilter(tags_all=['a_tag', 'not_here']))
        assert len(results) == 0

    def test_query_by_filter_tags_all_2_1(self):
        engine = Helpers.setup_everything2(FixturesLoader.load_questions_with_tags)
        fetcher = Sqlite3Reader(engine=engine)
        results = fetcher.load(ItemRegistryFilter(tags_all=['not_here', 'a_tag']))
        assert len(results) == 0

    def test_query_by_filter_tags_all_3(self):
        engine = Helpers.setup_everything2(FixturesLoader.load_questions_with_tags)
        fetcher = Sqlite3Reader(engine=engine)
        results = fetcher.load(ItemRegistryFilter(tags_all=['a_tag', 'b_tag']))
        assert len(results) == 2

    def test_query_by_filter_difficulty(self):
        engine = Helpers.setup_everything2(FixturesLoader.load_questions_with_tags)
        fetcher = Sqlite3Reader(engine=engine)
        results = fetcher.load(ItemRegistryFilter(difficulty_category='Hard'))
        assert len(results) == 0

    def test_query_by_filter_difficulty(self):
        engine = Helpers.setup_everything2(FixturesLoader.load_questions_with_tags)
        fetcher = Sqlite3Reader(engine=engine)
        results = fetcher.load(ItemRegistryFilter(difficulty_category='Easy'))
        assert len(results) == 3
