class LocalFileSystemReader:
    def load(self, models) -> None:
        for model in models:
            with open(model.src_filename, "r") as f:
                model.function_src = f.read()
