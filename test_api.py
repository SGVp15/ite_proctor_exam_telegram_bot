import asyncio

from Ispring.ispring2 import IspringApi
from selenium_for_proctoredu import Proctor


async def test_ispring():
    IspringApi().get_user()
    print("[test] Ispring OK")


async def test_proctoredu():
    drive = Proctor()
    await drive.authorization()
    drive.quit()
    print("[test] ProctorEDU OK")


async def main():
    task1 = asyncio.create_task(test_proctoredu())
    task2 = asyncio.create_task(test_ispring())
    await task1
    await task2


if __name__ == '__main__':
    asyncio.run(main())
