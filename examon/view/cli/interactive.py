from examon.lib.config.examon_config import ExamonConfig
from examon.lib.config.examon_config_json_init import ExamonConfigJsonInit
from examon.lib.config.examon_config_directory_init import ExamonConfigDirectoryInit
from examon.lib.examon_engine_factory import ExamonEngineFactory
from examon.lib.pip_installer import PipInstaller
from examon.lib.results_manager import ResultsManager
from examon.lib.settings_manager_factory import SettingsManagerFactory
from examon.lib.storage.question_factory import QuestionFactory
from examon.view.formatter_options import FormatterOptions

from examon_core.examon_item_registry import ExamonItemRegistry, ItemRegistryFilter
from simple_term_menu import TerminalMenu
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
        examon_config = ExamonConfig()
        manager = InteractiveCLI.setup(examon_config)

        examon_engine, results_manager = InteractiveCLI.run_quiz(
            examon_config, manager, ItemRegistryFilter(
                tags_any=(InteractiveCLI.get_tags())
            )
        )
        full_results_file_path = f'{examon_config.results_full_path()}/{ResultsManager.default_filename()}'
        results_manager.save_to_file(full_results_file_path)
        print(f'Results saved to {full_results_file_path}')

        print(examon_engine.summary())

    @staticmethod
    def setup(examon_config):
        path = examon_config.config_full_file_path()
        ExamonConfigJsonInit.persist_default_config(path)
        ExamonConfigDirectoryInit.init_everything(examon_config)
        manager = SettingsManagerFactory.build(path)
        for package in InteractiveCLI.DEFAULT_PACKAGES:
            manager.add(package)
            manager.add_active(package)
        ExamonConfigJsonInit.persist(manager, path)
        PipInstaller.install(manager.packages)
        PipInstaller.import_packages(manager.active_packages)
        return manager

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
    def run_quiz(examon_config, manager, registry_filter):
        questions = QuestionFactory.load(manager.mode, examon_config, registry_filter)
        examon_engine = ExamonEngineFactory.build(
            questions, FormatterOptions()['terminal256'])
        examon_engine.run()
        results_manager = ResultsManager(examon_engine.responses,
                                         manager.active_packages,
                                         registry_filter)
        return examon_engine, results_manager
