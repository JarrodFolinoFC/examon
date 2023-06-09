import argparse
from examon.view.formatter_options import FormatterOptions

class ExamonArgParse:
    def __init__(self, parser, formatter_options):
        self.__parser = parser
        self.__formatter_options = formatter_options
        self.__setup_args()

    def parse(self):
        return self.__parser.parse_args()

    def __setup_args(self):
        subparsers = self.__parser.add_subparsers(help='Manage question repositories', dest='command')
        repo_subparser = subparsers.add_parser('repo',
                                               help='Manage question repositories',
                                               aliases=['repos', 'repository', 'repositories'])
        repo_subparser.add_argument('sub_command', help='[add|remove|list|init|help]')
        repo_subparser.add_argument('--name', help='pip repository module name')
        repo_subparser.add_argument('--pip-url', help='pip repository module name')

        subparsers.add_parser('help', help='Print this message')

        run_subparser = subparsers.add_parser('run', help='Run the quiz')
        run_subparser.add_argument("--formatter", help='')
        run_subparser.add_argument("--tag", help='')

        subparsers.add_parser('tag',
                              help='Tag Information',
                              aliases=['tags'])

        subparsers.add_parser('overview',
                              help='Tag Information',
                              aliases=['tags'])

class ExamonArgParseFactory:
    @staticmethod
    def build():
        parser = argparse.ArgumentParser(prog='Examon CLI')
        cli_args = ExamonArgParse(parser, FormatterOptions()).parse()
        return (parser, cli_args)
