from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from examon.lib.ingester.db.models.question import Question


class Sqlite3Driver:
    def __init__(self, db_file, models) -> None:
        self.engine = create_engine(f"sqlite+pysqlite:///{db_file}", echo=True)
        self.models = models

    def run(self):
        question_db_models = []
        with Session(self.engine) as session:
            for model in self.models:
                question_db_models.append(
                    Question(
                        unique_id=model.unique_id,
                        internal_id=model.internal_id,
                        version=1,
                        repository=None,
                        language="python",
                        src_filename=model,
                        created_at=model
                    )
                )
            session.add_all(question_db_models)
            session.commit()
