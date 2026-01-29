import datetime
import secrets

import jwt

from ProctorEDU.config import SECRET_GEN_LINK_PROCTOREDU, HOST_PROCTOREDU


def generate_proctoring_link(
        subject: str,
        username: str,
        nickname: str,
        members: str = '',
        tags: str = '',
        identifier: str = '',
        template: str = '',
        expires_in_hours: int = 500,
        host=HOST_PROCTOREDU,
        secret: str = SECRET_GEN_LINK_PROCTOREDU,
        provider: str = 'jwt',
) -> str:
    """
    nickname=email
    Генерирует ссылку для прокторинга с использованием JWT.
    """
    if not identifier:
        identifier = secrets.token_hex(16)

    # 1. Формируем данные (payload) из заголовков и значений
    data: dict
    data['template'] = template
    data['identifier'] = identifier
    data['subject'] = subject
    data['members'] = members
    data['tags'] = tags
    data['username'] = username
    data['nickname'] = nickname

    # 2. Настраиваем время истечения (exp) и выпуска (iat)
    now = datetime.datetime.now()
    expiration_time = now + datetime.timedelta(hours=expires_in_hours)

    # Добавляем стандартные поля JWT к пользовательским данным
    payload = {
        "iat": int(now.timestamp()),
        "exp": int(expiration_time.timestamp())
    }
    payload.update(data)

    # 3. Создаем токен (HS256 используется по умолчанию в PyJWT при передаче алгоритма)
    token = jwt.encode(payload, secret, algorithm='HS256')

    # В новых версиях PyJWT encode возвращает строку, в старых — bytes.
    # Приводим к строке на всякий случай.
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    # 4. Формируем финальную ссылку
    return f"https://{host}/api/auth/{provider}?token={token}"
