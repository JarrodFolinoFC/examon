import os
import pytest
from examon_core.examon_item_registry import ExamonItemRegistry
from examon_core.models.question import BaseQuestion, MultiChoiceQuestion
from examon.lib.storage.write.question_adapter_factory import build
from examon.lib.storage.write.ingest_factory import IngestFactory
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from helpers import Helpers
from fixtures_loader import FixturesLoader

from examon.lib.storage.drivers.content.sql_db.models.models import Question


@pytest.fixture(autouse=True)
def run_around_tests():
    Helpers.clean()
    current_working_directory = os.getcwd()
    test_db_name = Helpers.test_db(current_working_directory)
    IngestFactory.build(f'{current_working_directory}/tests/tmp/files',
                        test_db_name, ExamonItemRegistry.registry()).run()
    yield
    Helpers.clean()


class TestBuild:
    def test_build_base_question(self):
        FixturesLoader.load_q1()
        question = ExamonItemRegistry.registry()[0]
        build1 = build(question)
        assert build1.__class__ == BaseQuestion
        assert build1.internal_id == 'question_one'

    def test_build_multichoice_question(self):
        FixturesLoader.load_multichoice()
        question = ExamonItemRegistry.registry()[0]
        build1 = build(question)
        assert build1.__class__ == MultiChoiceQuestion
        assert build1.internal_id == 'question_one'
        assert build1.choices == ['1', '2', '3']

    def test_build_db_question_with_choices(self):
        test_db_name = Helpers.run_ingester(FixturesLoader.load_multichoice)
        engine = create_engine(f"sqlite+pysqlite:///{test_db_name}", echo=True)
        with Session(engine) as session:
            stmt = select(Question).where(Question.internal_id == 'question_one')
            for question in session.scalars(stmt, 0):
                build1 = build(question)
                assert build1.choices == ['1', '2', '3']

    def test_build_db_question(self):
        test_db_name = Helpers.run_ingester(FixturesLoader.load_q1)
        engine = create_engine(f"sqlite+pysqlite:///{test_db_name}", echo=True)
        with Session(engine) as session:
            stmt = select(Question).where(Question.internal_id == 'question_one')
            for question in session.scalars(stmt, 0):
                build1 = build(question)
                assert build1.__class__ == BaseQuestion
                assert build1.internal_id == 'question_one'
                assert build1.unique_id == '94906873137099624396142246939254'
                assert build1.print_logs == ['1']
                assert build1.tags == ['a', 'b']
                assert build1.metrics.lloc == 3
                assert build1.metrics.loc == 4
                assert build1.metrics.sloc == 3
                assert build1.metrics.no_of_functions == 1
                assert build1.metrics.difficulty == 0.0
                assert build1.metrics.categorised_difficulty == 'Easy'
