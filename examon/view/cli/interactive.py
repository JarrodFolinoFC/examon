from examon_core.examon_item_registry import ExamonItemRegistry, ItemRegistryFilter
from simple_term_menu import TerminalMenu

from examon.lib.pip_installer import PipInstaller
from examon.lib.config.config_dir_factory import ConfigDirFactory
from examon.lib.examon_engine_factory import ExamonEngineFactory
from examon.lib.storage.read.examon_reader_factory import ExamonReaderFactory
from examon.lib.reporting.results_manager import ResultsManager
from examon.view.formatter_options import FormatterOptions
from ...lib.utils.logging import decorator_timer

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
    @decorator_timer
    def process_command():
        print(ASCII_ART)
        examon_config_dir = ConfigDirFactory.init_everything(ConfigDirFactory.build())
        manager = PipInstaller.install(examon_config_dir)

        examon_engine, results_manager = InteractiveCLI.run_quiz(
            examon_config_dir, manager, ItemRegistryFilter(
                tags_any=(InteractiveCLI.get_tags())
            )
        )
        full_results_file_path = f'{examon_config_dir.results_full_path()}/{ResultsManager.default_filename()}'
        results_manager.save_to_file(full_results_file_path)
        print(f'Results saved to {full_results_file_path}')

        print(examon_engine.summary())

    @staticmethod
    def get_tags():
        available_tags = list(filter(None, ExamonItemRegistry.unique_tags()))
        selected_tags = None
        if len(available_tags) > 0:
            terminal_menu = TerminalMenu(
                available_tags,
                title='Please select the question tags',
                multi_select=True,
                show_multi_select_hint=True,
            )
            terminal_menu.show()
            selected_tags = [*terminal_menu.chosen_menu_entries]
        return selected_tags

    @staticmethod
    def run_quiz(examon_config_dir, manager, registry_filter):
        questions = ExamonReaderFactory.load(examon_config_dir, examon_filter=registry_filter)
        examon_engine = ExamonEngineFactory.build(
            questions, FormatterOptions()['terminal256'])
        examon_engine.run()
        results_manager = ResultsManager(examon_engine.responses,
                                         manager.active_packages,
                                         registry_filter)
        return examon_engine, results_manager
