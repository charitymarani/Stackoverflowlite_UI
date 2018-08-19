'''checker.py'''
from Stackoverflowlite.models import ALL_QUESTIONS


def question_already_exist(id):
    ''' check if an object exist'''
    if id in ALL_QUESTIONS:
        print('Question already exists')
    return False


def answer_already_exist(list_, object_key, object_attr):
    ''' find out if an object exist'''
    object_list = list(
        filter(
            lambda object_dict: object_dict[object_key] == object_attr,
            list_))
    if object_list:
        return object_list
    return False
