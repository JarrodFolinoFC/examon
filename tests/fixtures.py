from examon_core.examon_item import examon_item


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


def load_all():
    load_q1()
    load_q2()


def load_q1():
    @examon_item(internal_id='question_one', tags=['a', 'b'],
                 repository='myrepo')
    def question_1():
        return 1


def load_q1_duplicate_tags():
    @examon_item(internal_id='question_one', tags=['a', 'a', 'b'])
    def question_1():
        return 1


def load_q2():
    @examon_item(internal_id='question_two', tags=['a', 'b'])
    def question_2():
        return 2


def load_q3_with_prints():
    @examon_item(internal_id='question_three', tags=['a', 'b'])
    def question_2():
        print('a')
        print('b')
        print('c')
        return 2


def load_q3_with_choices():
    @examon_item(internal_id='question_three', choices=['1', '2', '3'],
                 tags=['a', 'b'])
    def question_2():
        return 2
