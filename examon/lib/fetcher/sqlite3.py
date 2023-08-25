from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from ..ingester.db.models.models import Question, Tag, Metrics
from ..ingester.question_adapter_factory import build


class Sqlite3Fetcher:
    def __init__(self, db_file=None, filename_strategy=None) -> None:
        self.engine = create_engine(f"sqlite+pysqlite:///{db_file}", echo=True)
        self.filename_strategy = filename_strategy

    def load(self, examon_filter=None):
        def array_contains_all(array, has_one):
            return len(intersection(array, has_one)) == len(has_one)

        def intersection(lst1, lst2):
            return list(set(lst1) & set(lst2))

        with Session(self.engine) as session:
            query = session.query(Question). \
                join(Question.tags). \
                join(Question.metrics). \
                join(Question.print_logs)

            if examon_filter is not None and examon_filter.tags_any is not None:
                query = query.filter(or_(*[Tag.value == tag for tag in examon_filter.tags_any]))

            if examon_filter is not None and examon_filter.difficulty_category is not None:
                query = query.filter(Metrics.categorised_difficulty == examon_filter.difficulty_category)

            question_models = [build(q) for q in query.all()]

            if examon_filter is not None and examon_filter.tags_all is not None:
                filtered_results = []
                for question_model in question_models:
                    if array_contains_all(question_model.tags, examon_filter.tags_all):
                        filtered_results.append(question_model)
                question_models = filtered_results

            return question_models
