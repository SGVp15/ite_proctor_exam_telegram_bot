import asyncio
import time

from Itexpert.ite_api import ITEXPERT_API
from ProctorEDU.selenium_for_proctoredu import ProctorEduSelenium


async def test_proctoredu():
    drive = ProctorEduSelenium()
    await drive.authorization()
    drive.quit()
    print("[test] ProctorEDU OK")


async def main():
    task1 = asyncio.create_task(test_proctoredu())
    await task1


if __name__ == '__main__':
    # asyncio.run(main())
    # 4. Тестирование удаления экзамена
    for id_exam_delete in range(28528, 28535 + 1):
        time.sleep(1)
        print(f"\n[4. delete_exam_by_id({id_exam_delete})]")
        r_delete = ITEXPERT_API().delete_exam_by_id(id_exam_delete)
        print("Результат удаления:", r_delete.status_code)
