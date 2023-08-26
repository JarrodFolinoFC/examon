import os


class LocalFileSystemDriver:
    def __init__(self, filename_strategy=None, models=None):
        self.filename_strategy = filename_strategy
        self.models = models

    def create_files(self):
        for model in self.models:
            full_file_path = self.filename_strategy.name(model)
            full_dirname = os.path.dirname(full_file_path)
            if not os.path.exists(full_dirname):
                os.makedirs(full_dirname)
            f = open(full_file_path, "w")
            f.write(model.function_src)
            f.close()

    def delete_files(self):
        for model in self.models:
            filename = self.filename_strategy.name(model)
            if os.path.exists(filename):
                # os.remove(filename)
                pass

