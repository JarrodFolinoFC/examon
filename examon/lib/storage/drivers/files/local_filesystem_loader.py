class LocalFileSystemLoader:
    def __init__(self, path):
        self.path = path

    def load(self, models):
        for model in models:
            with open(model.src_filename, "r") as f:
                model.function_src = f.read()
