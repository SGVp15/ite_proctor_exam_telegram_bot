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
    ite_api = ITEXPERT_API()
    for id_exam_delete in (28555,28554,28553,28541 ):
        time.sleep(1)
        print(f"\n[4. delete_exam_by_id({id_exam_delete})]")
        r_delete = ITEXPERT_API().delete_exam_by_id(id_exam_delete)
        print("Результат удаления:", r_delete.status_code)

    # # 2. Тестирование получения экзамена по ID
    # for id_exam in [28312, 28313]:
    #     print(f"\n[2. get_exam_by_id({id_exam})]")
    #     r_id = ite_api.get_exam_by_id(id_exam)
    #     if r_id and r_id.ok:
    #         pprint(json.loads(r_id.text))
    #     else:
    #         print("Не удалось получить экзамен по ID.")
    #
    # # 3. Тестирование создания экзамена
    # print(f"\n[3. create_exam({contact})]")
    # r_create = ite_api.create_exam(contact)
    # if r_create:
    #     print("Результат создания:", r_create.status_code)
    #
    # # 4. Тестирование удаления экзамена
    # for id_exam_delete in (28505,28506,28507,28508,28509,28510):
    #     print(f"\n[4. delete_exam_by_id({id_exam_delete})]")
    #     r_delete = ite_api.delete_exam_by_id(id_exam_delete)
    #     print("Результат удаления:", r_delete.status_code)
        # print(f"\n[get_exam_by_email({email})]")
        # r_id = ite_api.get_exam_by_email(email)
        # if r_id and r_id.ok:
        #     pprint(json.loads(r_id.text))
        # else:
        #     print("Не удалось получить экзамен по ID.")