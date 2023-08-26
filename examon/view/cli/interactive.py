from examon.lib.examon_config import ExamonConfig
from examon.lib.examon_engine_factory import ExamonEngineFactory
from examon.view.formatter_options import FormatterOptions
from examon.lib.results_manager import ResultsManager

from examon.lib.pip_installer import PipInstaller
from examon_core.examon_item_registry import ExamonItemRegistry, ItemRegistryFilter
from simple_term_menu import TerminalMenu
from examon.lib.package_manager_factory import PackageManagerFactory

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
        path = ExamonConfig().config_full_file_path()
        PackageManagerFactory.persist_default_config(path)

        manager = PackageManagerFactory.load(path)
        for package in InteractiveCLI.DEFAULT_PACKAGES:
            manager.add(package)
            manager.add(package)
            manager.add_active(package)

        PackageManagerFactory.persist(manager, path)
        PipInstaller.install(manager.packages)
        PipInstaller.import_packages(manager.active_packages)

        InteractiveCLI.init_everything(ExamonConfig())

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
        questions = ExamonItemRegistry.registry(registry_filter)

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
    def init_everything(examon_config, clean=False):
        import os
        import shutil
        from examon.lib.ingester.ingest_factory import IngestFactory

        db_full_file_path = examon_config.sqlite3_full_path()
        dirname = os.path.dirname(db_full_file_path)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        if not os.path.isfile(db_full_file_path):
            from pathlib import Path

            current_dir = Path(__file__)
            examon_dir = [p for p in current_dir.parents if p.parts[-1] == 'examon'][0]
            shutil.copy(f'{examon_dir}/../resources/examon.db', db_full_file_path)

        code_files_dir = examon_config.code_files_dir()
        IngestFactory.build(code_files_dir, db_full_file_path,
                            ExamonItemRegistry.registry()).run()

