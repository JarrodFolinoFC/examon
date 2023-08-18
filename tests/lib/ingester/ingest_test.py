import os
import shutil
import uuid
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from examon.lib.ingester.db.models.models import Question
from examon.lib.ingester.ingest_factory import IngestFactory
from examon_core.examon_item import examon_item
from examon_core.examon_item_registry import ExamonItemRegistry


import pytest


def load_all():
    load_q1()
    load_q2()


def load_q1():
    @examon_item(internal_id='question_one', tags=['a', 'b'],
                 repository='myrepo')
    def question_1():
        return 1


def load_q1_duplicate_tags():
    @examon_item(internal_id='question_one', tags=['a', 'a', 'b'])
    def question_1():
        return 1


def load_q2():
    @examon_item(internal_id='question_two', tags=['a', 'b'])
    def question_2():
        return 2


def load_q3_with_prints():
    @examon_item(internal_id='question_three', tags=['a', 'b'])
    def question_2():
        print('a')
        print('b')
        print('c')
        return 2


def load_q3_with_choices():
    @examon_item(internal_id='question_three', choices=['1', '2', '3'],
                 tags=['a', 'b'])
    def question_2():
        return 2


def test_db():
    current_working_directory = os.getcwd()
    src_file = f'{current_working_directory}/tests/empty.test.db'
    destination = f'{current_working_directory}/tests/tmp/test.{uuid.uuid4()}.db'
    shutil.copy(src_file, destination)
    return destination


@pytest.fixture(autouse=True)
def run_around_tests():
    ExamonItemRegistry.reset()
    yield
    ExamonItemRegistry.reset()
    current_working_directory = os.getcwd()
    # shutil.rmtree(f'{current_working_directory}/tests/tmp/*.db')


class TestIngest:
    def run_ingester(self, f):
        f()
        test_db_name = test_db()
        IngestFactory.build('/tmp', test_db_name).run()
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
                assert question.src_filename == '/tmp/myrepo/24610570444134442526585499076789.py'

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
