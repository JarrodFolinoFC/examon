import pytest
import os
import json

from examon.lib.reporting.results_manager import ResultsManager

from examon_core.models.question_response import QuestionResponse
from examon_core.models.question import BaseQuestion
from examon_core.models.code_metrics import CodeMetrics
from helpers import Helpers


def build_qr():
    function_src = """
def question():
    return 1
"""
    return QuestionResponse(BaseQuestion(
        unique_id='abc',
        internal_id='123',
        function_src=function_src,
        tags=['a'],
        print_logs=['1'],
        correct_answer=None,
        metrics=CodeMetrics(function_src),
    ),
        response='3', correct=False)


class TestResultManager:
    def test_creates_valid_json(self):
        Helpers.setup_directories()
        packages = ['package_a']
        question_responses = [build_qr()]
        examon_filter = None
        results_manager = ResultsManager([question_responses], packages, examon_filter)
        filename = f'{os.getcwd()}/tests/tmp/.examon/results/results.json'

        results_manager.save_to_file(filename)
        with open(filename, 'r') as file:
            json.load(file)
