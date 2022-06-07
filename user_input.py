import requests
from sql_consts import SQL_CONSTS
import ast
#
# mother_details = {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value:'1111',SQL_CONSTS.WOMEN_DETAILS_COLUMNS.FULL_NAME.value:'Woman 1', SQL_CONSTS.WOMEN_DETAILS_COLUMNS.PASSWORD.value: '123456'}
# #requests.post(url='http://localhost:9000/save_woman_details/',json=mother_details)
#
# child={SQL_CONSTS.CHILDREN_DETAILS.IDENTIFIER.value : '1234', SQL_CONSTS.CHILDREN_DETAILS.MOTHER_ID.value:'1111'}
# requests.post(url='http://localhost:9000/save_child_details/',json=child)

#register_data = {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value:'8888',SQL_CONSTS.WOMEN_DETAILS_COLUMNS.PASSWORD.value: 'password', SQL_CONSTS.WOMEN_DETAILS_COLUMNS.FULL_NAME.value:'shira'}
#requests.post(url='http://localhost:9000/register/',json=register_data)
login_data = {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value:'8888',SQL_CONSTS.WOMEN_DETAILS_COLUMNS.PASSWORD.value: 'password'}
response = requests.post(url='http://localhost:9000/login/',json=login_data)
response_str = response.content.decode()
response_body = ast.literal_eval(response_str)
jwt_token = response_body['access_token']
woman_details_response = requests.get(url='http://localhost:9000/get_woman_details/8888', headers = {"Authorization":'Bearer '+jwt_token });
