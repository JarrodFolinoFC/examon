from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from ..ingester.db.models.models import Question, PrintLog
from ..ingester.question_adapter_factory import build


class Sqlite3Fetcher:
    def __init__(self, db_file=None, filename_strategy=None, models=None) -> None:
        self.engine = create_engine(f"sqlite+pysqlite:///{db_file}", echo=True)
        self.models = models
        self.filename_strategy = filename_strategy

    def load(self, filter=None):
        with Session(self.engine) as session:
            results = []
            stmt = select(Question, PrintLog).join(PrintLog.print_logs)
            for row in session.execute(stmt):
                results.append(build(row))
            return results
