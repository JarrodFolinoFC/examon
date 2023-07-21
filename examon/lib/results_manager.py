from dataclasses_serialization.json import JSONSerializer
from datetime import datetime


class ResultsManager:
    def __init__(self, question_responses, filters=None, file_name=None):
        self.question_responses = question_responses
        if file_name is None:
            self.file_name = f'{datetime.now().strftime("%d%m%Y%H%M")}_results.json'
        else:
            self.file_name = file_name

    def save_to_file(self):
        serialized = JSONSerializer.serialize(
            {
                'responses': self.question_responses
            }
        )
        with open(self.file_name, "w") as outfile:
            outfile.write(str(serialized))
