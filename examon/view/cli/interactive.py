from examon.lib.config.examon_config import ExamonConfig
from examon.lib.config.examon_config_json_init import ExamonConfigJsonInit
from examon.lib.config.examon_config_directory_init import ExamonConfigDirectoryInit
from examon.lib.examon_engine_factory import ExamonEngineFactory
from examon.lib.results_manager import ResultsManager
from examon.view.formatter_options import FormatterOptions
from examon.lib.pip_installer import PipInstaller
from examon.lib.package_manager_factory import PackageManagerFactory
from examon.lib.storage.fetcher.fetch import Fetch
from examon.lib.storage.fetcher.sqlite3_fetcher import Sqlite3Fetcher

from examon_core.examon_item_registry import ExamonItemRegistry, ItemRegistryFilter
from simple_term_menu import TerminalMenu

ASCII_ART = """
              ,--.
              |
              |-   . , ,-: ;-.-. ,-. ;-.
              |     X  | | | | | | | | |
              `--' ' ` `-` ' ' ' `-' ' '
        """


class InteractiveCLI:
    DEFAULT_PACKAGES = ['examon_beginners_package']

    @staticmethod
    def process_command():
        print(ASCII_ART)
        examon_config = ExamonConfig()
        path = examon_config.config_full_file_path()
        ExamonConfigJsonInit.persist_default_config(path)
        ExamonConfigDirectoryInit.init_everything(examon_config)

        manager = PackageManagerFactory.build(path)
        for package in InteractiveCLI.DEFAULT_PACKAGES:
            manager.add(package)
            manager.add(package)
            manager.add_active(package)

        ExamonConfigJsonInit.persist(manager, path)
        PipInstaller.install(manager.packages)
        PipInstaller.import_packages(manager.active_packages)

        available_tags = list(filter(None, ExamonItemRegistry.unique_tags()))
        all_tags_filter = None
        if len(available_tags) > 0:
            terminal_menu = TerminalMenu(
                available_tags,
                title='Please select the question tags',
                multi_select=True,
                show_multi_select_hint=True,
            )
            terminal_menu.show()
            all_tags_filter = [*terminal_menu.chosen_menu_entries]

        registry_filter = ItemRegistryFilter(tags_any=all_tags_filter)

        # check mode
        questions = InteractiveCLI.load_qs(examon_config, registry_filter)
        examon_engine = ExamonEngineFactory.build(
            questions, FormatterOptions()['terminal256'])
        examon_engine.run()
        results_manager = ResultsManager(examon_engine.responses,
                                         manager.active_packages,
                                         registry_filter)
        results_manager.save_to_file()
        print(f'Results saved to {results_manager.full_path}')

        print(examon_engine.summary())

    @staticmethod
    def load_qs(examon_config, examon_filter):
        class FileLoader:
            def __init__(self, models):
                self.models = models

            def load(self):
                for model in self.models:
                    with open(self.path, "r") as f:
                        model.function_src = f.read()

        record_driver = Sqlite3Fetcher(
            db_file=examon_config.sqlite3_full_path()
        )
        blob_driver = FileLoader
        fetch = Fetch(record_driver, blob_driver)
        return fetch.load(examon_filter)
