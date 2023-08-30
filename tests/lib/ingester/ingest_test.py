import pytest

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from examon_core.examon_item_registry import ExamonItemRegistry

from examon.lib.storage.read_write.sql_db import Question
from helpers import Helpers
from fixtures_loader import FixturesLoader


@pytest.fixture(autouse=True)
def run_around_tests():
    ExamonItemRegistry.reset()
    yield
    ExamonItemRegistry.reset()
    Helpers.clean()


class TestWriter:

    def test_creates_question_record(self):
        import os
        with Session(Helpers.setup_everything2(FixturesLoader.load_q1)) as session:
            stmt = select(Question).where(Question.internal_id == 'question_one')
            for question in session.scalars(stmt, 0):
                assert question.internal_id == 'question_one'
                assert question.version == 1
                assert question.language == 'python'
                assert question.unique_id == '94906873137099624396142246939254'
                # assert question.src_filename == f'{os.getcwd()}/tests/tmp/files/myrepo/94906873137099624396142246939254.py'
                assert os.path.exists(question.src_filename)

    def test_creates_question_tags_record(self):
        with Session(Helpers.setup_everything2(FixturesLoader.load_q1)) as session:
            stmt = select(Question).where(Question.internal_id == 'question_one')
            for question in session.scalars(stmt, 0):
                assert list(map(lambda x: x.value, question.tags)) == ['a', 'b']

    def test_creates_question_with_metrics(self):
        with Session(Helpers.setup_everything2(FixturesLoader.load_q3_with_choices)) as session:
            stmt = select(Question).where(Question.internal_id == 'question_three')
            for question in session.scalars(stmt, 0):
                assert question.metrics.no_of_functions == 1
                assert question.metrics.loc == 4
                assert question.metrics.lloc == 3
                assert question.metrics.sloc == 3
                assert question.metrics.difficulty == 0.0

    def test_creates_multiple_records_dupes(self):
        engine = Helpers.setup_everything2(FixturesLoader.load_all)
        with Session(engine) as session:
            assert session.query(func.count(Question.id)).scalar() == 2

    def test_creates_multiple_records(self):
        with Session(Helpers.setup_everything2(FixturesLoader.load_all)) as session:
            assert session.query(func.count(Question.id)).scalar() == 2

    def test_creates_question_with_prints_logs_record(self):
        with Session(Helpers.setup_everything2(FixturesLoader.load_q3_with_prints)) as session:
            stmt = select(Question).where(Question.internal_id == 'question_three')
            for question in session.scalars(stmt, 0):
                assert list(map(lambda x: (x.value, x.log_number), question.print_logs)) == \
                       [('a', 0), ('b', 1), ('c', 2), ('2', 3)]

    def test_creates_question_with_choices_record(self):
        with Session(Helpers.setup_everything2(FixturesLoader.load_q3_with_choices)) as session:
            stmt = select(Question).where(Question.internal_id == 'question_three')
            for question in session.scalars(stmt, 0):
                assert list(map(lambda x: x.value, question.choices)) == \
                       ['1', '2', '3']

    # def test_creates_question_tags_record_with_duplicate(self):
    #     test_db_name = Helpers.run_ingester(load_q1_duplicate_tags)
    #     engine = create_engine(f"sqlite+pysqlite:///{test_db_name}", echo=True)
    #     with Session(engine) as session:
    #         stmt = select(Question).where(Question.internal_id == 'question_one')
    #         for question in session.scalars(stmt, 0):
    #             assert list(map(lambda x: x.value, question.tags)) == ['a', 'b']
