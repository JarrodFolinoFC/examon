from examon.lib.config.config_structure import ExamonConfigStructure
from examon.lib.config.config_structure_factory import ConfigStructureFactory
from examon.lib.config.json_config_store import JsonConfigStore
from examon.lib.config.settings_manager_factory import SettingsManagerFactory
from examon.lib.storage.ingester.ingest_factory import IngestFactory
from examon.lib.pip_installer import PipInstaller

from examon_core.examon_item_registry import ExamonItemRegistry
from examon.lib.config.config_structure import ExamonConfigStructure
from .validate_config import ValidateConfig

class PackageManagerCli:
    @staticmethod
    def process_command(cli_args):
        config = ExamonConfigStructure(settings_file='config.json')
        path = config.config_full_file_path()
        sub_command = cli_args.sub_command

        if sub_command == 'init':
            ConfigStructureFactory.init_everything()
            return

        ValidateConfig.config_dir_exists(config)

        package_manager = SettingsManagerFactory.build(path)
        if sub_command in ['add', 'remove', 'add_active', 'remove_active']:
            if sub_command == 'add':
                package_manager.add(cli_args.name, cli_args.pip_url)
            elif sub_command == 'remove':
                package_manager.remove(cli_args.name)
            elif sub_command == 'add_active':
                package_manager.add_active(cli_args.name)
            elif sub_command == 'remove_active':
                package_manager.remove_active(cli_args.name)
            JsonConfigStore.persist(package_manager, path)
            return

        if sub_command == 'list':
            PackageManagerCli.print_packages(package_manager)
        elif sub_command == 'install':
            PipInstaller.install(package_manager.packages)
            PipInstaller.import_packages([package['name'] for package in package_manager.packages])
            if package_manager.mode == 'sqlite3':
                IngestFactory.build(f"{config.examon_dir}/files",
                                    f'{config.examon_dir}/examon.db',
                                    ExamonItemRegistry.registry()).run()

        else:
            print('Invalid subcommand (add, remove, install, list, init)')

    @staticmethod
    def print_packages(package_manager):
        print('')
        print('All:')
        for repo in package_manager.packages:
            print(repo['name'])
        print('')
        print('Active:')
        for repo in package_manager.active_packages:
            print(repo)
        print('')
