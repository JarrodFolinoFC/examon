from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    unique_id: Mapped[str]
    internal_id: Mapped[str]
    version: Mapped[int]
    repository: Mapped[Optional[str]]
    language: Mapped[Optional[str]]
    src_filename: Mapped[Optional[str]]
    created_at: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Question(id={self.id!r}, " \
               f"unique_id={self.unique_id!r}, " \
               f"internal_id={self.fullname!r}, " \
               f"version={self.fullname!r}, " \
               f"repository={self.fullname!r}, " \
               f"language={self.fullname!r}, " \
               f"src_filename={self.fullname!r}, " \
               f"created_at={self.fullname!r})"

