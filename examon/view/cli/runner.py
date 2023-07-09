from lib.quiz_engine_factory import build_quiz_engine
from examon.lib.repo_manager import RepoManager
from view.formatter_options import FormatterOptions

class RunnerCli:
    @staticmethod
    def process_command(cli_args):
        manager = RepoManager()
        manager.load()
        manager.import_repos()
        quiz_engine = build_quiz_engine(cli_args.tag, FormatterOptions()[cli_args.formatter])
        quiz_engine.run()
        print(quiz_engine.summary())
