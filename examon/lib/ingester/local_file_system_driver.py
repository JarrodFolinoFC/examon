class LocalFileSystemDriver:
    def __init__(self, filename_strategy=None, models=None):
        self.filename_strategy = filename_strategy
        self.models = models

    def create_files(self):
        pass

    def delete_files(self):
        pass
