# import re
#
# import requests
# from loguru import logger
# from lxml import etree
# from requests.structures import CaseInsensitiveDict
#
# from config_ispring import Config
#
#
# class ApiRequest:
#     def init(self, new_user) -> None:
#         self.base_url = Config.base_url
#         self.headers = CaseInsensitiveDict()
#         self.headers["Host"] = Config.Host
#         self.headers["X-Auth-Account-Url"] = Config.X_Auth_Account_Url
#         self.headers["X-Auth-Email"] = Config.X_Auth_Email
#         self.headers["X-Auth-Password"] = Config.X_Auth_Password
#         self.new_user = new_user
#         self.default_department_id = Config.default_department_id
#         self.dueDate = Config.dueDate
#         self.re_login = re.compile(r'(?P<login>\w+)@', re.M | re.S)
#
#     def check_exist_user(self) -> bool:
#         """example of get request"""
#         url = f"{self.base_url}/user"
#         email = self.new_user.email
#         resp = requests.get(url, headers=self.headers)
#         if resp.status_code != 200:
#             raise ValueError(f"Request check_exist_user failed {resp.status_code}")
#         resp_xml_content = resp.content
#         tree = etree.XML(resp_xml_content)
#         user_by_email = tree.xpath(
#             f'/response/userProfile/fields/field[name = "EMAIL" and value = "{email}"]')
#         if user_by_email:
#             logger.info(f"Пользователя с email {email} еще не существует")
#             return False
#         logger.info(f"Пользователь с email {email} уже существует")
#         self.new_user.user_id = (tree.xpath(
#             f".//userProfile[./fields/field/name[contains(text(), 'EMAIL')] and ./fields/field/value[contains(text(), '{email}')]]/userId"))[
#             0].text
#         return True
#
#     def add_user(self) -> bool:
#         """example of post request"""
#         url = f"{self.base_url}/user"
#         login = self.re_login.search(self.new_user.email).group('login')
#
#         files = {
#             'departmentId': (None, f'{self.default_department_id}'),
#             'fields[email]': (None, f'{self.new_user.email}'),
#             'fields[login]': (None, f'{login}'),
#         }
#
#         response = requests.post(url=url, headers=self.headers, files=files)
#
#         if response.status_code != 201:
#             raise ValueError(f"Request add_user failed {response.status_code}")
#         resp_xml_content = resp.content
#         try:
#             self.new_user.user_id = etree.XML(resp_xml_content).text
#             logger.info(f"Add new user successful. User_id: {self.new_user.user_id}")
#             return True
#         except Exception as ex:
#             logger.error(f"Error get user_id from responce {ex}")
#             return False
