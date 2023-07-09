import argparse
import os.path
import os
import sys
from view.formatter_options import FormatterOptions
from view.input.quiz_arg_parse import QuizArgParse
from view.output.display_stats import display_stats
from lib.quiz_engine_factory import build_quiz_engine
from .repo_manager import RepoManager

DEFAULT_MODULE = 'examon_repo_1'
DEFAULT_FROM_LIST = '*'


class CliRuntime:

    @staticmethod
    def manager_instance():
        manager = RepoManager()
        manager.load()
        return manager

    @staticmethod
    def process_repo_command(cli_args):
            if cli_args.sub_command == 'add':
                manager = CliRuntime.manager_instance()
                manager.add(cli_args.name, cli_args.pip_url)
                manager.persist()
            elif cli_args.sub_command == 'install':
                CliRuntime.manager_instance().install()
            elif cli_args.sub_command == 'remove':
                manager = CliRuntime.manager_instance()
                manager.remove(cli_args.name)
                manager.remove_active(cli_args.name)
                manager.persist()
            elif cli_args.sub_command == 'list':
                manager = CliRuntime.manager_instance()
                print('All:')
                for repo in manager.repos:
                    print(repo)

                print('')

                print('Active:')
                for repo in manager.active_repos:
                    print(repo)

            elif cli_args.sub_command == 'init':
                manager = CliRuntime.manager_instance()
                if os.path.isfile(manager.full_file_path()):
                    print(f'{manager.full_file_path()} already exists')
                else:
                    manager.persist_default()
                    print(f'{manager.full_file_path()} created')


    @staticmethod
    def run():
        parser = argparse.ArgumentParser(prog='Examon CLI', description='Manages your exam items')
        cli_args = QuizArgParse(parser, FormatterOptions()).parse()

        if cli_args.command == 'run':
                manager = CliRuntime.manager_instance()
                manager.import_repos()
                quiz_engine = build_quiz_engine(cli_args.tag, FormatterOptions()[cli_args.formatter])
                quiz_engine.run()
                print(quiz_engine.summary())
        elif cli_args.command == 'overview':
                print('overview')
                quiz_engine = build_quiz_engine(None, None)
                display_stats(quiz_engine.stats())
        elif cli_args.command in ['repo', 'repos']:
                CliRuntime.process_repo_command(cli_args)
        elif cli_args.command == 'help':
                parser.print_help()



        # except:
        #     parser.print_help()
        # finally:
        #     sys.exit(0)
