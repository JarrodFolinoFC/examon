from examon_core.models.question import BaseQuestion
from .protocols import FileReader, ContentReader


class Reader:
    def __init__(self, content_reader: ContentReader, file_reader: FileReader):
        self.content_reader = content_reader
        self.file_reader = file_reader

    def load(self, examon_filter=None) -> list[BaseQuestion]:
        models = self.content_reader.load(examon_filter)
        self.file_reader.load(models)
        return models
