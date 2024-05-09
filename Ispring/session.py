class Session:
    def __init__(self, enrollment_dict, user_dict, course_dict):
        self.enrollment_id = enrollment_dict.get('enrollmentId')
        self.access_date = enrollment_dict.get('accessDate')
        self.course_name = course_dict.get('title')
        self.username = f'{user_dict.get('LAST_NAME')} {user_dict.get('FIRST_NAME')}'
        self.user_email = user_dict.get('EMAIL')

    def __str__(self):
        return f'{self.access_date} {self.course_name} {self.username} {self.user_email}'

    def __gt__(self, other):
        return f'{self.access_date}' > f'{other.access_date}'
