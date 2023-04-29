import argparse
from view.formatter_options import FormatterOptions
from view.input.quiz_arg_parse import QuizArgParse
from view.output.display_stats import display_stats
from lib.quiz_engine_factory import build_quiz_engine


class CliRuntime:
    @staticmethod
    def run():
        cli_args = QuizArgParse(argparse.ArgumentParser(), FormatterOptions()).parse()
        CliRuntime.load_module(cli_args)
        quiz_engine = build_quiz_engine(cli_args.tag, FormatterOptions()[cli_args.formatter])

        if cli_args.command == 'run':
            quiz_engine.run()
            print(quiz_engine.summary())
        elif cli_args.command == 'overview':
            display_stats(quiz_engine.stats())
        else:
            print(cli_args)

    @staticmethod
    def load_module(cli_args):
        if cli_args.pip_module is None:
            return
        elif cli_args.pip_from_list is None:
            __import__(cli_args.pip_module, fromlist=['*'])
        else:
            __import__(cli_args.pip_module, fromlist=cli_args.pip_from_list.split(','))
