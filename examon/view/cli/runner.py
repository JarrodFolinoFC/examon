from examon.lib.examon_engine_factory import ExamonEngineFactory
from examon.lib.package_manager import PackageManager
from examon.lib.results_manager import ResultsManager
from examon.view.formatter_options import FormatterOptions
from examon_core.examon_item_registry import ItemRegistryFilter


class RunnerCli:
    @staticmethod
    def process_command(cli_args):
        manager = PackageManager()
        manager.load()
        manager.import_packages()
        item_registry = ItemRegistryFilter(tags_any=[cli_args.tag])
        examon_engine = ExamonEngineFactory.build(
            item_registry, FormatterOptions()[
                cli_args.formatter])
        examon_engine.run()
        if cli_args.file:
            ResultsManager(examon_engine.responses, cli_args.file).save_to_file()
            print(f'Results saved to {cli_args.file}')
        print(examon_engine.summary())
