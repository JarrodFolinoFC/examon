import os
from pygments import highlight
from pygments.lexers import PythonLexer


class BaseQuestionOutputter():
    def __init__(self, formatter_class):
        self.formatter_class = formatter_class

    def print_metrics(self, question):
        print(f'Difficulty: {question.metrics.calc_difficulty()}')

    def present_summary(self, summary):
        os.system('clear')
        print(f'You are: {summary}')

    def present_question(self, question):
        print(
            highlight(
                question.function_src,
                PythonLexer(),
                self.formatter_class()))

    def display_print_logs(self, question):
        if len(question.print_logs) > 1:
            print('Print logs:')
            for log in question.print_logs:
                print(f' - {log.output}')
            print('')


class InputParameterQuestionOutputter(BaseQuestionOutputter):
    def present_question(self, question):
        print('')
        self.print_metrics(question)
        print('')
        super().present_question(question)
        print('')
        test = 'What does the parameter need to be for'\
               ' the last print statement to return:'
        print(test)
        print(question.return_value)
        print('')
        print('')
        self.display_print_logs(question)


class ExpectedResultQuestionOutputter(BaseQuestionOutputter):
    def present_question(self, question):
        print('')
        self.print_metrics(question)
        print('What is the result of the last print statement?')
        print('')
        super().present_question(question)
        print('')
        self.display_print_logs(question)


class FreeTextQuestionOutputter(BaseQuestionOutputter):
    def present_question(self, question):
        print('')
        self.print_metrics(question)
        print('')
        super().present_question(question)
        print('')
        print('What will this return?')
        print('')
        self.display_print_logs(question)
