'''checker.py'''
def already_exist(list_, object_key, object_attr):
    ''' check if an object exist'''
    object_list = list(
        filter(
            lambda object_dict: object_dict[object_key] == object_attr,
            list_))
    if object_list:
        return object_list
    return False

