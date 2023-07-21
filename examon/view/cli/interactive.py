from examon.lib.package_manager import PackageManager
from examon.lib.examon_engine_factory import ExamonEngineFactory
from examon.view.formatter_options import FormatterOptions
from examon.lib.results_manager import ResultsManager

from simple_term_menu import TerminalMenu

from examon_core.examon_item_registry import ExamonItemRegistry, ItemRegistryFilter


class InteractiveCLI:
    DEFAULT_PACKAGES = ['examon_beginners_package']

    @staticmethod
    def process_command():
        print("""
              ,--.                       
              |                          
              |-   . , ,-: ;-.-. ,-. ;-. 
              |     X  | | | | | | | | | 
              `--' ' ` `-` ' ' ' `-' ' '
        """)
        manager = PackageManager()
        for package in InteractiveCLI.DEFAULT_PACKAGES:
            manager.add(package)

        print('Please select 1 or more packages')
        terminal_menu = TerminalMenu(
            InteractiveCLI.DEFAULT_PACKAGES,
            multi_select=True,
            show_multi_select_hint=True,
        )
        terminal_menu.show()


        for active in list(terminal_menu.chosen_menu_entries):
            manager.add(active)
            manager.add_active(active)
        manager.persist()

        manager.load()
        manager.install()
        manager.import_packages()

        print('Please select the question tags')
        terminal_menu = TerminalMenu(
            ExamonItemRegistry.unique_tags(),
            multi_select=True,
            show_multi_select_hint=True,
        )
        terminal_menu.show()

        registry_filter = ItemRegistryFilter(tags_any=terminal_menu.chosen_menu_entries)

        examon_engine = ExamonEngineFactory.build(
            registry_filter, FormatterOptions()['terminal256'])
        examon_engine.run()
        results_manager = ResultsManager(examon_engine.responses)
        results_manager.save_to_file()
        print(f'Results saved to {results_manager.file_name}')

        print(examon_engine.summary())
