from ..protocols import FileReader


class LocalFileSystemReader(FileReader):

    def load(self, models: list) -> None:
        for model in models:
            with open(model.src_filename, "r") as f:
                model.function_src = f.read()
