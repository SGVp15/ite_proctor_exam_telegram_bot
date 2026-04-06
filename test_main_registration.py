import asyncio

from main_registration import sheduler_registration_server_file


def test_sheduler_registration_server_file():
    asyncio.run(sheduler_registration_server_file())
    # assert False

