from typing_extensions import Protocol

from examon_core.models.question import BaseQuestion


class FilenameStrategy(Protocol):
    def name(self, model: BaseQuestion) -> str: ...


class SimpleFilenameStrategy(FilenameStrategy):
    def __init__(self, base_path) -> None:
        self.base_path = base_path

    def name(self, model) -> str:
        return f"{self.base_path}/{model.repository}/{model.unique_id}.py"
