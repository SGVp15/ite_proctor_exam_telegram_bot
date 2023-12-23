class User:
    def __init__(self, first_name_ru: str, last_name_ru: str, first_name_en: str, last_name_en: str, email: str,
                 password: str = ''):
        self.first_name_ru = first_name_ru
        self.last_name_ru = last_name_ru
        self.first_name_en = first_name_en
        self.last_name_en = last_name_en
        self.email = email

        self.login = f'{self.last_name_en}_{self.first_name_en}'
        if password != '':
            self.password = password
        else:
            self.password = f'{self.login}_123'
