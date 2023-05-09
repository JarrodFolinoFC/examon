import os
from pygments import highlight
from pygments.lexers import PythonLexer

class BaseQuestionOutputter():
    def __init__(self, formatter_class):
        self.formatter_class = formatter_class

    def present_summary(self, summary):
        os.system('clear')
        print(f'You are: {summary}')

    def present_question(self, question):
        print(
            highlight(
                question.function_src,
                PythonLexer(),
                self.formatter_class()))


class InputParameterQuestionOutputter(BaseQuestionOutputter):
    def present_question(self, question):
        print('')
        print('')
        super().present_question(question)
        print('')
        print('What does the parmeter need to be for the last print statement to return:')
        print(question.return_value)
        print('')
        print('')


class ExpectedResultQuestionOutputter(BaseQuestionOutputter):
    def present_question(self, question):
        print('')
        print('What is the result of the last print statement?')
        print('')
        super().present_question(question)
        print('')
        if len(question.print_logs) > 1:
            print('Print logs (last print omitted):')
            for log in question.print_logs[:-1]:
                print(log[0])
            print('')


class FreeTextQuestionOutputter(BaseQuestionOutputter):
    def present_question(self, question):
        print('')
        print('')
        super().present_question(question)
        print('')
        print('What will this return?')
