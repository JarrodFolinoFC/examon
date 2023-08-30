from functools import singledispatch

from examon_core.models.question import BaseQuestion, MultiChoiceQuestion
from examon_core.models.code_metrics import CodeMetrics
from ..read_write.sql_db import Question


@singledispatch
def build(question) -> list[BaseQuestion]:
    raise Exception('NotSupported')


@build.register(BaseQuestion)
def _(question) -> list[BaseQuestion]:
    return question


@build.register(MultiChoiceQuestion)
def _(question) -> list[BaseQuestion]:
    return question


@build.register(Question)
def _(question) -> list[BaseQuestion]:
    klass = None
    if len(question.choices) == 0:
        klass = BaseQuestion
    elif len(question.choices) > 0:
        klass = MultiChoiceQuestion

    question_model = klass(
        internal_id=question.internal_id,
        unique_id=question.unique_id,
        print_logs=[q.value for q in question.print_logs],
        tags=[q.value for q in question.tags],
        correct_answer=question.answer,
        metrics=CodeMetrics(code_as_string="",
                            lloc=question.metrics.lloc,
                            loc=question.metrics.loc,
                            sloc=question.metrics.sloc,
                            no_of_functions=question.metrics.no_of_functions,
                            difficulty=question.metrics.difficulty,
                            categorised_difficulty=question.metrics.categorised_difficulty
                            )
    )
    question_model.src_filename = question.src_filename

    if question_model.__class__ == MultiChoiceQuestion:
        question_model.choices = [q.value for q in question.choices]

    return question_model
