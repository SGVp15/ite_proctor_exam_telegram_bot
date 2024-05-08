import xmltodict


def get_ispring_users(s: str) -> list[dict]:
    my_dict = xmltodict.parse(s)

    users_from_ispring: list = my_dict.get('response').get('userProfile')

    for user in users_from_ispring:
        fields: list = user.get('fields').get('field')

        for field in fields:
            user[field.get('name')] = field.get('value')

    return users_from_ispring


def get_ispring_enrollment(s: str) -> list[dict]:
    my_dict = xmltodict.parse(s)
    enrollments_ispring: list = my_dict.get('response').get('enrollment')
    return enrollments_ispring
