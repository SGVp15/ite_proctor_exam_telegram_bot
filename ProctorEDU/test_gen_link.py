from unittest import TestCase

from ProctorEDU.gen_link import generate_proctoring_link


class Test(TestCase):
    def test_generate_proctoring_link(self):
        # 1. Исходные данные
        provider = "jwt"

        expires = 500
        subject: str = 'Test-2026-01-29-3'
        username: str = 'Tes_username'
        nickname: str = 'Test_nickname'

        # 2. Генерация ссылки
        link = generate_proctoring_link(subject=subject, username=username,
                                        nickname=nickname, provider=provider, expires_in_hours=expires)
        print(link)


if __name__ == '__main__':
    import unittest

    unittest.main()
