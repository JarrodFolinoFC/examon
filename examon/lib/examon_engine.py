from examon_core.question_response import QuestionResponse
from examon.lib.streak_tracker import StreakTracker


class ExamonEngine:
    def __init__(self, questions=None,
                 stats_outputter=None,
                 view_mappings=None):
        self.questions = questions
        self.correct_answers = 0
        self.responses = []
        self.__streak = StreakTracker()

        self.__view_mappings = view_mappings
        self.__stats_outputter = stats_outputter

    def run(self):
        for question in self.questions:
            lookup_key = question.__class__.__name__
            self.display(lookup_key, question)
            choice = self.get_user_input(lookup_key, question)
            correct = question.answer(choice)
            if correct:
                self.correct_answers += 1
                self.__streak.increment()
            else:
                self.__streak.reset()

            self.responses.append(QuestionResponse(question, choice, correct))

        self.final_summary()

    def get_user_input(self, lookup_key, question):
        return self.__view_mappings[lookup_key]['inputter'].prompt(question)

    def display(self, lookup, question):
        self.__view_mappings[lookup]['outputter'].present_summary(
            (self.summary()))
        self.__view_mappings[lookup]['outputter'].present_question(question)
        return lookup

    def final_summary(self):
        correct, no = self.summary()
        print(f'You scored:\t{correct} / {no}')
        self.__streak.reset()
        print(f'Best Streak:\t{self.__streak.summary()}')

    def summary(self):
        return self.correct_answers, len(self.questions)

    def stats(self):
        return self.__stats_outputter(self.questions)
