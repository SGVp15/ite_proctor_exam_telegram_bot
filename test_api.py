import asyncio

from ProctorEDU.selenium_for_proctoredu import ProctorEduSelenium


async def test_proctoredu():
    drive = ProctorEduSelenium()
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
