from examon_core.question import *
from examon_core.examon_item_registry import *

from view.input.answer_question import AnswerInputter, FreeTextAnswerInputter
from view.output.question import *
from .calc_stats import calc_stats
from .quiz_engine import QuizEngine

def build_quiz_engine(tag, formatter_class):
    registry = ExamonItemRegistry.registry(tag)
    view_mappings = {
        ExpectedResultQuestion.__name__: {
            'outputter': ExpectedResultQuestionOutputter(formatter_class),
            'inputter': AnswerInputter()
        },
        InputParameterQuestion.__name__: {
            'outputter': InputParameterQuestionOutputter(formatter_class),
            'inputter': AnswerInputter()
        }, BaseQuestion.__name__: {
            'outputter': FreeTextQuestionOutputter(formatter_class),
            'inputter': FreeTextAnswerInputter()
        }
    }
    return QuizEngine(
        questions=registry,
        view_mappings=view_mappings,
        stats_outputter=calc_stats)