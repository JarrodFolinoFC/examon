from simple_term_menu import TerminalMenu

class AnswerInputter:
    def __init__(
            self,
            message="Enter Choice: "):
        self.__message = message

    def prompt(self, question):
        choices = list(map(str, question.choices))
        terminal_menu = TerminalMenu(choices)
        menu_entry_index = terminal_menu.show()
        return question.choices[menu_entry_index]

class FreeTextAnswerInputter:
    def prompt(self, _question):
        return input('Enter your answer\n\n')
