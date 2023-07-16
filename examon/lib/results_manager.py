from dataclasses_serialization.json import JSONSerializer


class ResultsManager:
    def __init__(self, question_responses, file_name):
        self.question_responses = question_responses
        self.file_name = file_name

    def save_to_file(self):
        serialized = JSONSerializer.serialize(self.question_responses)
        with open(self.file_name, "w") as outfile:
            outfile.write(str(serialized))
