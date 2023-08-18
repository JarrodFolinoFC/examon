from examon_core.models.question import BaseQuestion, MultiChoiceQuestion, \
    InputParameterQuestion
from examon_core.examon_item_registry import ExamonItemRegistry

from examon.view.input.answer_question import AnswerInputter, \
    FreeTextAnswerInputter
from examon.view.output.question import MultiChoiceQuestionOutputter, \
    InputParameterQuestionOutputter, FreeTextQuestionOutputter
from .stats import Stats
from .examon_engine import ExamonEngine


class ExamonEngineFactory:
    @staticmethod
    def build(examon_filter, formatter_class, auto_answer=None, shuffle=False):
        def fetch_inputter(enabled, inputter):
            return enabled if enabled else inputter

        if shuffle:
            ExamonItemRegistry.shuffle()

        registry = ExamonItemRegistry.registry(examon_filter)
        view_mappings = {
            MultiChoiceQuestion.__name__: {
                'outputter': MultiChoiceQuestionOutputter(formatter_class),
                'inputter': fetch_inputter(auto_answer, AnswerInputter())
            },
            InputParameterQuestion.__name__: {
                'outputter': InputParameterQuestionOutputter(formatter_class),
                'inputter': fetch_inputter(auto_answer, AnswerInputter())
            }, BaseQuestion.__name__: {
                'outputter': FreeTextQuestionOutputter(formatter_class),
                'inputter': fetch_inputter(
                    auto_answer, FreeTextAnswerInputter())
            }
        }
        return ExamonEngine(
            questions=registry,
            view_mappings=view_mappings,
            stats_outputter=Stats.calc_stats)
