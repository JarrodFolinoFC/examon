class SimpleFilenameStrategy:
    def __init__(self, base_path):
        self.base_path = base_path

    def name(self, model):
        return f"{self.base_path}/{model.repository}/{model.unique_id}.py"
