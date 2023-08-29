from dataclasses_serialization.json import JSONStrSerializer
from datetime import datetime


class ResultsManager:
    def __init__(self, question_responses, packages,
                 examon_filter) -> None:
        self.question_responses = question_responses
        self.packages = packages
        self.examon_filter = examon_filter

    def save_to_file(self, full_file_path) -> None:
        serialized = JSONStrSerializer.serialize(
            {
                "date": datetime.now().strftime("%d%m%Y%H%M"),
                "packages": self.packages,
                "filters": self.examon_filter,
                "responses": self.question_responses
            }
        )
        with open(full_file_path, "w") as outfile:
            outfile.write(str(serialized))

    @staticmethod
    def default_filename() -> str:
        return f'{datetime.now().strftime("%d%m%Y%H%M")}_results.json'
