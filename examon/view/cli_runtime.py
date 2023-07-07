import argparse
import os.path
import os
from view.formatter_options import FormatterOptions
from view.input.quiz_arg_parse import QuizArgParse
from view.output.display_stats import display_stats
from lib.quiz_engine_factory import build_quiz_engine
from .repo_manager import RepoManager

DEFAULT_MODULE = 'examon_repo_1'
DEFAULT_FROM_LIST = '*'

class CliRuntime:
    @staticmethod
    def run():
        cli_args = QuizArgParse(argparse.ArgumentParser(
            prog='Examon CLI',
            description='Manages your exam items'
        ), FormatterOptions()).parse()

        if cli_args.command == 'run':
            manager = RepoManager()
            manager.load()
            manager.import_repos()
            quiz_engine = build_quiz_engine(cli_args.tag, FormatterOptions()[cli_args.formatter])
            quiz_engine.run()
            print(quiz_engine.summary())
        elif cli_args.command == 'overview':
            print('overview')
            quiz_engine = build_quiz_engine(None, None)
            display_stats(quiz_engine.stats())
        elif cli_args.command == 'repo':
            CliRuntime.process_repo_command(cli_args)
        else:
            print(cli_args)

    @staticmethod
    def process_repo_command(cli_args):
        if cli_args.sub_command == 'add':
            manager = RepoManager()
            manager.load()
            manager.add(cli_args.name, cli_args.pip_url)
            manager.persist()
        elif cli_args.sub_command == 'remove':
            manager = RepoManager()
            manager.load()
            manager.remove(cli_args.name)
            manager.remove_active(cli_args.name)
            manager.persist()
        elif cli_args.sub_command == 'list':
            manager = RepoManager()
            manager.load()

            print('All:')
            for repo in manager.repos:
                print(repo)

            print('')

            print('Active:')
            for repo in manager.active_repos:
                print(repo)

        elif cli_args.sub_command == 'init':
            if os.path.isfile(RepoManager.full_file_path()):
                print(f'{RepoManager.full_file_path()} already exists')
            else:
                RepoManager.persist_default()
                print(f'{RepoManager.full_file_path()} created')
