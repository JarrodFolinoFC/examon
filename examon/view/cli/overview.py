from examon.lib.stats import Stats
from examon.lib.examon_engine_factory import ExamonEngineFactory


class OverviewCli:
    @staticmethod
    def process_command():
        print('overview')
        quiz_engine = ExamonEngineFactory.build(None, None)
        Stats.display_stats(quiz_engine.stats())
