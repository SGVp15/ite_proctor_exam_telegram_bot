import xmltodict


def get_ispring_users(s: str) -> list[dict]:
    my_dict = xmltodict.parse(s)
    users_ispring: list = my_dict.get('response').get('userProfile')
    for user in users_ispring:
        fields: list = user.get('fields').get('field')
        for field in fields:
            user[field.get('name')] = field.get('value')
    return users_ispring


def get_ispring_enrollments(s: str) -> list[dict]:
    my_dict = xmltodict.parse(s)
    enrollments_ispring = my_dict.get('response').get('enrollment')
    if type(enrollments_ispring) is dict:
        return [enrollments_ispring, ]
    return enrollments_ispring


def get_ispring_contents(s: str) -> list[dict]:
    my_dict = xmltodict.parse(s)
    contents_ispring: list = my_dict.get('response').get('contentItem')
    return contents_ispring
