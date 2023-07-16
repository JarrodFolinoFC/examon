from examon.lib.examon_engine_factory import ExamonEngineFactory
from examon.lib.repo_manager import RepoManager
from examon.lib.results_manager import ResultsManager
from examon.view.formatter_options import FormatterOptions


class RunnerCli:
    @staticmethod
    def process_command(cli_args):
        manager = RepoManager()
        manager.load()
        manager.import_repos()
        examon_engine = ExamonEngineFactory.build(
            cli_args.tag, FormatterOptions()[
                cli_args.formatter])
        examon_engine.run()
        if cli_args.file:
            ResultsManager(examon_engine.responses, cli_args.file).save_to_file()
            print(f'Results saved to {cli_args.file}')
        print(examon_engine.summary())
