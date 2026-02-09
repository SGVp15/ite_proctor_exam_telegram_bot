import time

from Itexpert.ite_api import ITEXPERT_API

ite_api = ITEXPERT_API()
for id_exam_delete in (28562,):
    time.sleep(1)
    print(f"\n[4. delete_exam_by_id({id_exam_delete})]")
    r_delete = ITEXPERT_API().delete_exam_by_id(id_exam_delete)
    print("Результат удаления:", r_delete.status_code)