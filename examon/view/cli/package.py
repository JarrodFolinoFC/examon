import os.path
import os

from examon.lib.package_manager import PackageManager
from examon.lib.pip_installer import PipInstaller

class PackageManagerCli:
    @staticmethod
    def process_command(cli_args):
        package_manager = PackageManager()
        if cli_args.sub_command == 'add':
            package_manager.add(cli_args.name, cli_args.pip_url)
            package_manager.load()
            package_manager.persist()
        elif cli_args.sub_command == 'remove':
            package_manager.remove(cli_args.name)
            package_manager.load()
            package_manager.remove_active(cli_args.name)
            package_manager.persist()
        elif cli_args.sub_command == 'add_active':
            package_manager.add_active(cli_args.name)
            package_manager.load()
            package_manager.persist()
        elif cli_args.sub_command == 'remove_active':
            package_manager.remove_active(cli_args.name)
            package_manager.load()
            package_manager.persist()
        elif cli_args.sub_command == 'install':
            package_manager.load()
            PipInstaller.install(package_manager.packages)
        elif cli_args.sub_command == 'list':
            package_manager.load()
            print('')
            print('All:')
            for repo in package_manager.packages:
                print(repo['name'])
            print('')
            print('Active:')
            for repo in package_manager.active_packages:
                print(repo)
            print('')
        elif cli_args.sub_command == 'init':
            if os.path.isfile(package_manager.full_file_path):
                print(f'{package_manager.full_file_path} already exists')
            else:
                package_manager.persist_default_config()
                print(f'{package_manager.full_file_path } created')
        else:
            print('Invalid subcommand (add, remove, install, list, init)')
