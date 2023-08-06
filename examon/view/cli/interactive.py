from examon.lib.package_manager import PackageManager
from examon.lib.examon_engine_factory import ExamonEngineFactory
from examon.view.formatter_options import FormatterOptions
from examon.lib.results_manager import ResultsManager

from examon.lib.pip_installer import PipInstaller
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
        manager = PackageManager()
        for package in InteractiveCLI.DEFAULT_PACKAGES:
            manager.add(package)

        terminal_menu = TerminalMenu(
            InteractiveCLI.DEFAULT_PACKAGES,
            title='Please select 1 or more packages',
            multi_select=True,
            show_multi_select_hint=True,
            multi_select_empty_ok=False
        )
        terminal_menu.show()

        for active in [*terminal_menu.chosen_menu_entries]:
            manager.add(active)
            manager.add_active(active)
        manager.persist()

        manager.load()
        PipInstaller.install(manager.packages)
        PipInstaller.import_packages(manager.active_packages)

        available_tags = ExamonItemRegistry.unique_tags()
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

        examon_engine = ExamonEngineFactory.build(
            registry_filter, FormatterOptions()['terminal256'])
        examon_engine.run()
        results_manager = ResultsManager(examon_engine.responses,
                                         manager.active_packages,
                                         registry_filter)
        results_manager.save_to_file()
        print(f'Results saved to {results_manager.full_path}')

        print(examon_engine.summary())
