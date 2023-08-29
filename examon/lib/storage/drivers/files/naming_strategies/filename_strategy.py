class SimpleFilenameStrategy:
    def __init__(self, base_path) -> None:
        self.base_path = base_path

    def name(self, model) -> str:
        return f"{self.base_path}/{model.repository}/{model.unique_id}.py"
