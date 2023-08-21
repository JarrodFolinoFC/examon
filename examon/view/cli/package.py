import os.path
import os

from examon.lib.package_manager_factory import PackageManagerFactory
from examon.lib.pip_installer import PipInstaller
from examon.lib.examon_config import ExamonConfig


class PackageManagerCli:
    @staticmethod
    def process_command(cli_args):
        path = ExamonConfig().full_file_path()
        package_manager = PackageManagerFactory.load(path)
        sub_command = cli_args.sub_command

        if sub_command in ['add', 'remove', 'add_active', 'remove_active']:
            if sub_command == 'add':
                package_manager.add(cli_args.name, cli_args.pip_url)
            elif sub_command == 'remove':
                package_manager.remove(cli_args.name)
            elif sub_command == 'add_active':
                package_manager.add_active(cli_args.name)
            elif sub_command == 'remove_active':
                package_manager.remove_active(cli_args.name)
            PackageManagerFactory.persist(package_manager, path)
            return

        if sub_command == 'list':
            PackageManagerCli.print_packages(package_manager)
        elif sub_command == 'init':
            if os.path.isfile(path):
                print(f'{path} already exists')
            else:
                PackageManagerFactory.persist_default_config(path)
                print(f'{path} created')
        elif sub_command == 'install':
            PipInstaller.install(package_manager.packages)
            # this is where we ingest
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
