from examon_core.examon_item import examon_item


class FixturesLoader:
    @staticmethod
    def load_questions_with_tags():
        @examon_item(tags=['a_tag'])
        def question_1():
            return 1

        @examon_item(tags=['a_tag', 'b_tag'])
        def question_2():
            return 1

        @examon_item(tags=['a_tag', 'b_tag', 'c_tag'])
        def question_3():
            return 1

    @staticmethod
    def load_mixed():
        @examon_item(tags=['a'])
        def question_1():
            return 1

        @examon_item(tags=['a'], choices=['1', '2', '3'])
        def question_1():
            return 2

    @staticmethod
    def load_fixtures():
        @examon_item(tags=['a'])
        def question_1():
            return 1

        @examon_item(tags=['a'])
        def question_2():
            return 2

        @examon_item(tags=['a'])
        def question_3():
            return 3

    @staticmethod
    def load_all():
        FixturesLoader.load_q1()
        FixturesLoader.load_q2()

    @staticmethod
    def load_q1():
        @examon_item(internal_id='question_one', tags=['a', 'b'],
                     repository='myrepo')
        def question_1():
            return 1

    @staticmethod
    def load_multichoice():
        @examon_item(internal_id='question_one', tags=['a', 'b'],
                     choices=['1', '2', '3'],
                     repository='myrepo')
        def question_1():
            return 1

    @staticmethod
    def load_q1_duplicate_tags():
        @examon_item(internal_id='question_one', tags=['a', 'a', 'b'])
        def question_1():
            return 1

    @staticmethod
    def load_q2():
        @examon_item(internal_id='question_two', tags=['a', 'b'])
        def question_2():
            return 2

    @staticmethod
    def load_q3_with_prints():
        @examon_item(internal_id='question_three', tags=['a', 'b'])
        def question_2():
            print('a')
            print('b')
            print('c')
            return 2

    @staticmethod
    def load_q3_with_choices():
        @examon_item(internal_id='question_three', choices=['1', '2', '3'],
                     tags=['a', 'b'])
        def question_2():
            return 2
