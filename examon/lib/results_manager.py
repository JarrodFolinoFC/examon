from dataclasses_serialization.json import JSONSerializer
from datetime import datetime

from .examon_config import ExamonConfig


class ResultsManager:
    def __init__(self, question_responses, packages,
                 examon_filter, file_name=None):
        self.question_responses = question_responses
        self.packages = packages
        self.examon_filter = examon_filter
        if file_name is None:
            self.file_name = f'{datetime.now().strftime("%d%m%Y%H%M")}_results.json'
        else:
            self.file_name = file_name
        self.full_path = f'{ExamonConfig().examon_dir}/{self.file_name}'

    def save_to_file(self):
        serialized = JSONSerializer.serialize(
            {
                'date': datetime.now().strftime("%d%m%Y%H%M"),
                'packages': self.packages,
                'filters': self.examon_filter,
                'responses': self.question_responses
            }
        )
        ExamonConfig.create_config_folder()
        with open(f'{ExamonConfig().examon_dir}/{self.file_name}', "w") as outfile:
            outfile.write(str(serialized))
