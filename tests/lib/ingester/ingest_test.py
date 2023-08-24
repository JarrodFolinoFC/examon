import os
import shutil
import uuid
import pytest

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from examon.lib.ingester.db.models.models import Question
from examon.lib.ingester.ingest_factory import IngestFactory
from examon_core.examon_item_registry import ExamonItemRegistry

from ...fixtures import *


def test_db():
    current_working_directory = os.getcwd()
    src_file = f'{current_working_directory}/tests/empty.test.db'
    destination = f'{current_working_directory}/tests/tmp/db/test.{uuid.uuid4()}.db'
    shutil.copy(src_file, destination)
    return destination


@pytest.fixture(autouse=True)
def run_around_tests():
    ExamonItemRegistry.reset()
    yield
    ExamonItemRegistry.reset()
    current_working_directory = os.getcwd()
    for file in os.scandir(f'{current_working_directory}/tests/tmp/db'):
        if file.name.endswith(".db"):
            os.unlink(file.path)
    for directory in os.scandir(f'{current_working_directory}/tests/tmp/files'):
        if os.path.isdir(directory):
            shutil.rmtree(directory)


class TestIngest:
    def run_ingester(self, f):
        f()
        current_working_directory = os.getcwd()
        test_db_name = test_db()
        IngestFactory.build(f'{current_working_directory}/tests/tmp/files', test_db_name,
                            ExamonItemRegistry.registry()).run()
        return test_db_name

    def test_creates_multiple_records(self):
        test_db_name = self.run_ingester(load_all)
        engine = create_engine(f"sqlite+pysqlite:///{test_db_name}", echo=True)
        with Session(engine) as session:
            assert session.query(func.count(Question.id)).scalar() == 2

    def test_creates_question_record(self):
        test_db_name = self.run_ingester(load_q1)
        engine = create_engine(f"sqlite+pysqlite:///{test_db_name}", echo=True)
        with Session(engine) as session:
            stmt = select(Question).where(Question.internal_id == 'question_one')
            for question in session.scalars(stmt, 0):
                assert question.internal_id == 'question_one'
                assert question.version == 1
                assert question.language == 'python'
                assert question.unique_id == '24610570444134442526585499076789'
                assert question.src_filename == '/Users/jarrod.folino/Dev/examon_proj/examon/tests/tmp/files/myrepo/24610570444134442526585499076789.py'

                assert os.path.exists(question.src_filename)

    def test_creates_question_tags_record(self):
        test_db_name = self.run_ingester(load_q1)
        engine = create_engine(f"sqlite+pysqlite:///{test_db_name}", echo=True)
        with Session(engine) as session:
            stmt = select(Question).where(Question.internal_id == 'question_one')
            for question in session.scalars(stmt, 0):
                assert list(map(lambda x: x.value, question.tags)) == ['a', 'b']

    def test_creates_question_with_prints_logs_record(self):
        test_db_name = self.run_ingester(load_q3_with_prints)
        engine = create_engine(f"sqlite+pysqlite:///{test_db_name}", echo=True)
        with Session(engine) as session:
            stmt = select(Question).where(Question.internal_id == 'question_three')
            for question in session.scalars(stmt, 0):
                assert list(map(lambda x: (x.value, x.log_number), question.print_logs)) == \
                       [('a', 0), ('b', 1), ('c', 2), ('2', 3)]

    def test_creates_question_with_choices_record(self):
        test_db_name = self.run_ingester(load_q3_with_choices)
        engine = create_engine(f"sqlite+pysqlite:///{test_db_name}", echo=True)
        with Session(engine) as session:
            stmt = select(Question).where(Question.internal_id == 'question_three')
            for question in session.scalars(stmt, 0):
                assert list(map(lambda x: x.value, question.choices)) == \
                       ['1', '2', '3']

    def test_creates_question_with_metrics(self):
        test_db_name = self.run_ingester(load_q3_with_choices)
        engine = create_engine(f"sqlite+pysqlite:///{test_db_name}", echo=True)
        with Session(engine) as session:
            stmt = select(Question).where(Question.internal_id == 'question_three')
            for question in session.scalars(stmt, 0):
                assert question.metrics.no_of_functions == 1
                assert question.metrics.loc == 4
                assert question.metrics.lloc == 3
                assert question.metrics.sloc == 3
                assert question.metrics.difficulty == 0.0

    # def test_creates_question_tags_record_with_duplicate(self):
    #     test_db_name = self.run_ingester(load_q1_duplicate_tags)
    #     engine = create_engine(f"sqlite+pysqlite:///{test_db_name}", echo=True)
    #     with Session(engine) as session:
    #         stmt = select(Question).where(Question.internal_id == 'question_one')
    #         for question in session.scalars(stmt, 0):
    #             assert list(map(lambda x: x.value, question.tags)) == ['a', 'b']
