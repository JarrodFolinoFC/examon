import sys
import signal
import os

from examon.view.cli.examon_arg_parse import ExamonArgParseFactory
from examon.view.cli.runner import RunnerCli
from examon.view.cli.package import PackageManagerCli
from examon.view.cli.overview import OverviewCli
from examon.view.cli.interactive import InteractiveCLI


def handler(_signum, _frame):
    os.system('clear')
    print('Program terminated')
    sys.exit(0)


signal.signal(signal.SIGINT, handler)


def process_command():
    parser, cli_args = ExamonArgParseFactory.build()
    if cli_args.command == None:
        InteractiveCLI.process_command()
    if cli_args.command == 'run':
        RunnerCli.process_command(cli_args)
    elif cli_args.command == 'overview':
        OverviewCli.process_command()
    elif cli_args.command in ['package', 'packages']:
        PackageManagerCli.process_command(cli_args)
    elif cli_args.command == 'help':
        parser.print_help()

    sys.exit(0)
