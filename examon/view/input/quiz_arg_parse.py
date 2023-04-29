from collections import namedtuple

QuizArgs = namedtuple('QuizArgs', 'command tag formatter pip_module pip_from_list')


class QuizArgParse:
    def __init__(self, parser, formatter_options):
        self.__parser = parser
        self.__formatter_options = formatter_options
        self.__setup_args()

    def parse(self):
        args = self.__parser.parse_args()
        return QuizArgs(args.command, args.tag, args.formatter,
                        args.pip_module, args.pip_from_list
                        )

    def __setup_args(self):
        commands = [("command", "[run|overview]"),
                    ("--formatter", f'[{self.__formatter_options}]'),
                    ("--tag", '"overview" command will list all tags'),
                    ("--pip-module", "pip repository module name"),
                    ("--pip-from-list", "pip repository from list")
                    ]
        for command in commands:
            self.__parser.add_argument(command[0], help=command[1])
