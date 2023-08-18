from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from examon.lib.ingester.db.models.models import Question, Tag, PrintLog, Choice, Metrics
from examon_core.models.question import MultiChoiceQuestion
import datetime

LANGUAGE = 'python'


class Sqlite3Driver:
    def __init__(self, db_file=None, filename_strategy=None, models=None) -> None:
        self.engine = create_engine(f"sqlite+pysqlite:///{db_file}", echo=True)
        self.models = models
        self.filename_strategy = filename_strategy

    def create_all(self):
        question_db_models = []
        with Session(self.engine) as session:
            for model in self.models:
                version_number = 1
                repository = 'something'
                question_db_record = Question(unique_id=model.unique_id,
                                              internal_id=model.internal_id, version=version_number,
                                              src_filename=self.filename_strategy.name(model),
                                              repository=repository, language=LANGUAGE,
                                              created_at=datetime.datetime.now())

                question_db_record.metrics = Metrics(
                        no_of_functions=model.metrics.no_of_functions,
                        loc=model.metrics.loc,
                        lloc=model.metrics.lloc,
                        sloc=model.metrics.sloc,
                        difficulty=model.metrics.difficulty,

                        categorised_difficulty=model.metrics.categorised_difficulty
                )
                for tag in model.tags:
                    question_db_record.tags.append(Tag(value=tag))

                if model.__class__ == MultiChoiceQuestion:
                    for choice in model.choices:
                        question_db_record.choices.append(Choice(value=choice))

                for index, print_log in enumerate(model.print_logs):
                    question_db_record.print_logs.append(PrintLog(value=print_log, log_number=index))

                question_db_models.append(question_db_record)
                session.flush()
            session.add_all(question_db_models)

            session.commit()

    def delete_all(self):
        pass
