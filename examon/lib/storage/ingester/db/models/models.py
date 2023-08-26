from typing import Optional, List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column


class Base(DeclarativeBase):
    pass


class PrintLog(Base):
    __tablename__ = 'print_logs'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]
    log_number: Mapped[int]
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))

    def __repr__(self) -> str:
        return f"PrintLog(id={self.id!r}, " \
               f"value={self.value!r}, " \
               f"log_number={self.log_number!r}, " \
               f"question_id={self.question_id!r}"


class Tag(Base):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))

    def __repr__(self) -> str:
        return f"Tag(id={self.id!r}, " \
               f"value={self.value!r}, " \
               f"question_id={self.question_id!r}"


class Choice(Base):
    __tablename__ = 'choices'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))

    def __repr__(self) -> str:
        return f"Choice(id={self.id!r}, " \
               f"value={self.value!r}, " \
               f"question_id={self.question_id!r}"


class Metrics(Base):
    __tablename__ = 'metrics'
    id: Mapped[int] = mapped_column(primary_key=True)
    no_of_functions: Mapped[int]
    loc: Mapped[int]
    lloc: Mapped[int]
    sloc: Mapped[int]
    difficulty: Mapped[float]
    categorised_difficulty: Mapped[str]
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))

    def __repr__(self) -> str:
        return f"Metrics(id={self.id!r}, " \
               f"no_of_functions={self.no_of_functions!r}, " \
               f"loc={self.loc!r}, " \
               f"lloc={self.lloc!r}, " \
               f"sloc={self.sloc!r}, " \
               f"difficulty={self.difficulty!r}, " \
               f"categorised_difficulty={self.categorised_difficulty!r}, " \
               f"question_id={self.question_id!r}"


class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    unique_id: Mapped[str]
    internal_id: Mapped[str]
    version: Mapped[int]
    repository: Mapped[Optional[str]]
    language: Mapped[Optional[str]]
    answer: Mapped[str]
    src_filename: Mapped[str]
    created_at: Mapped[Optional[str]]
    tags: Mapped[List["Tag"]] = relationship()
    print_logs: Mapped[List["PrintLog"]] = relationship()
    choices: Mapped[List["Choice"]] = relationship()
    metrics: Mapped["Metrics"] = relationship()

    def __repr__(self) -> str:
        return f"Question(id={self.id!r}, " \
               f"unique_id={self.unique_id!r}, " \
               f"internal_id={self.internal_id!r}, " \
               f"version={self.version!r}, " \
               f"repository={self.repository!r}, " \
               f"language={self.language!r}, " \
               f"src_filename={self.src_filename!r}, " \
               f"created_at={self.created_at!r})"
