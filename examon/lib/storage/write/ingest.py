from .protocols import FileWriter


class Writer:
    def __init__(self, content_reader, file_writer: FileWriter) -> None:
        self.content_reader = content_reader
        self.file_writer = file_writer

    def run(self) -> None:
        try:
            self.content_reader.create_all()
            self.file_writer.create_files()
        except Exception:
            self.content_reader.delete_all()
            self.file_writer.delete_files()
            raise
