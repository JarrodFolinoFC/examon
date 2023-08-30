from typing_extensions import Protocol

from examon_core.models.question import BaseQuestion


class FilenameStrategy(Protocol):
    def name(self, model: BaseQuestion) -> str: ...


class FileWriter(Protocol):
    def create_files(self) -> None: ...

    def delete_files(self) -> None: ...


class ContentWriter(Protocol):
    def create_all(self) -> None: ...
