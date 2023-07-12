from examon.view.output.display_stats import display_stats
from examon.lib.quiz_engine_factory import QuizEngineFactory

class OverviewCli:
    @staticmethod
    def process_command():
        print('overview')
        quiz_engine = QuizEngineFactory.build(None, None)
        display_stats(quiz_engine.stats())
