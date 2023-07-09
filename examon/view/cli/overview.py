from view.output.display_stats import display_stats
from lib.quiz_engine_factory import build_quiz_engine

class OverviewCli:
    @staticmethod
    def process_command():
        print('overview')
        quiz_engine = build_quiz_engine(None, None)
        display_stats(quiz_engine.stats())
