from sqlalchemy import create_engine

class Sqlite3Driver:
    def __init__(self, db_file) -> None:
        self.engine = create_engine(f"sqlite+pysqlite:///{db_file}", echo=True)
    
    