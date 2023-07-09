import os.path
import os

from examon.lib.repo_manager import RepoManager

class RepoManagerCli:
    @staticmethod
    def process_command(cli_args):
        manager = RepoManager()
        manager.load()
        if cli_args.sub_command == 'add':
            manager.add(cli_args.name, cli_args.pip_url)
            manager.persist()
        elif cli_args.sub_command == 'install':
            manager.install()
        elif cli_args.sub_command == 'remove':
            manager.remove(cli_args.name)
            manager.remove_active(cli_args.name)
            manager.persist()
        elif cli_args.sub_command == 'list':
            print('All:')
            for repo in manager.repos:
                print(repo)
            print('')
            print('Active:')
            for repo in manager.active_repos:
                print(repo)

        elif cli_args.sub_command == 'init':
            if os.path.isfile(manager.full_file_path()):
                print(f'{manager.full_file_path()} already exists')
            else:
                manager.persist_default()
                print(f'{manager.full_file_path()} created')