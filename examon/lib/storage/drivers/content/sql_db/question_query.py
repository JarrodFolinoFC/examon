from sqlalchemy.orm import Session
from .models import Question


class QuestionQuery:
    def __init__(self, engine):
        self.engine = engine

    def question_unique_ids(self) -> list[str]:
        with Session(self.engine) as session:
            return [row.unique_id for row in session.query(Question)]
