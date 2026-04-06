import asyncio

from main_registration import server_file_registration


def test_sheduler_registration_server_file():
    asyncio.run(server_file_registration())
    # assert False

