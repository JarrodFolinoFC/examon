from examon_core.question import *
from examon_core.examon_item_registry import *

from examon.view.input.answer_question import AutoAnswerInputter, AnswerInputter, FreeTextAnswerInputter
from examon.view.output.question import *
from .calc_stats import calc_stats
from .quiz_engine import QuizEngine


class QuizEngineFactory:
    @staticmethod
    def build(tag, formatter_class, auto_answer=None):
        registry = ExamonItemRegistry.registry(tag)
        view_mappings = {
            ExpectedResultQuestion.__name__: {
                'outputter': ExpectedResultQuestionOutputter(formatter_class),
                'inputter': auto_answer if auto_answer else AnswerInputter()
            },
            InputParameterQuestion.__name__: {
                'outputter': InputParameterQuestionOutputter(formatter_class),
                'inputter': auto_answer if auto_answer else AnswerInputter()
            }, BaseQuestion.__name__: {
                'outputter': FreeTextQuestionOutputter(formatter_class),
                'inputter': auto_answer if auto_answer else FreeTextAnswerInputter()
            }
        }
        return QuizEngine(
            questions=registry,
            view_mappings=view_mappings,
            stats_outputter=calc_stats)
