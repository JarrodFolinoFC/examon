from examon_core.examon_item import examon_item
from examon.lib.quiz_engine_factory import build_quiz_engine
from examon.view.formatter_options import FormatterOptions
from examon.view.input.answer_question import AutoAnswerInputter
import pytest


@examon_item(tags=['a'])
def question_1():
    return 1


@examon_item(tags=['a'])
def question_2():
    return 2


@examon_item(tags=['a'])
def question_3():
    return 3


class TestEndToEnd:
    def test_e2e(self):
        inputter = AutoAnswerInputter([1, 2, 3])
        quiz_engine = build_quiz_engine('a', FormatterOptions()['null'], inputter)
        quiz_engine.run()
        assert quiz_engine.summary() == (3, 3)

    def test_e2e_2(self):
        inputter = AutoAnswerInputter([1, 2, 2])
        quiz_engine = build_quiz_engine('a', FormatterOptions()['null'], inputter)
        quiz_engine.run()
        assert quiz_engine.summary() == (2, 3)