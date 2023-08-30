from .protocols import FileWriter, ContentWriter


class Writer:
    def __init__(self, content_writer: ContentWriter, file_writer: FileWriter) -> None:
        self.content_writer = content_writer
        self.file_writer = file_writer

    def run(self) -> None:
        try:
            self.content_writer.create_all()
            self.file_writer.create_files()
        except Exception:
            self.file_writer.delete_files()
            raise
