import sys
from examon.view.cli.examon_arg_parse import ExamonArgParseFactory
from examon.view.cli.runner import RunnerCli
from examon.view.cli.repo import RepoManagerCli
from examon.view.cli.overview import OverviewCli


def process_command():
    parser, cli_args = ExamonArgParseFactory.build()
    if cli_args.command == 'run':
        RunnerCli.process_command(cli_args)
    elif cli_args.command == 'overview':
        OverviewCli.process_command()
    elif cli_args.command in ['repo', 'repos', 'repositories' 'repository']:
        RepoManagerCli.process_command(cli_args)
    elif cli_args.command == 'help':
        parser.print_help()

    sys.exit(0)
