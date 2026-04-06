import asyncio

from main_registration import scheduler_registration_server_file


def test_sheduler_registration_server_file():
    asyncio.run(scheduler_registration_server_file())
    # assert False

