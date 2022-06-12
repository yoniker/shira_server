import requests
from sql_consts import SQL_CONSTS
import ast
#
import datetime
import json
import random


from datetime import date, datetime

#So that we are able to convert datetime to json
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def login_as_woman_by_id(woman_id,password = '123456'):
    '''
    
    
    :param woman_id:
    :return:
    '''

    login_data = {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value:f'{woman_id}',SQL_CONSTS.WOMEN_DETAILS_COLUMNS.PASSWORD.value: password}
    response = requests.post(url='http://localhost:9000/login/',json=login_data)
    response_str = response.content.decode()
    response_body = ast.literal_eval(response_str)
    jwt_token = response_body['access_token']
    return jwt_token


# def fill_children_table(num_children = 10000, num_mothers = 999):
#
#
#     for i in range(1,num_children+1):
#         mother_id = random.randint(1,num_mothers)
#         jwt_token = login_as_woman_by_id(mother_id)
#         child_details={SQL_CONSTS.CHILDREN_DETAILS.IDENTIFIER.value : f'{i}', SQL_CONSTS.CHILDREN_DETAILS.MOTHER_ID.value:f'{mother_id}',
#                SQL_CONSTS.CHILDREN_DETAILS.BIRTHDAY.value: json.dumps(datetime(year=random.randint(2018,2022),month=random.randint(1,12),day=random.randint(1,28)),default=json_serial)
#                }
#         requests.post(url='http://localhost:9000/save_child_details/',json=child_details,headers = {"Authorization":'Bearer '+jwt_token})
#
# fill_children_table()


mother_details = {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value:f'777',
                  SQL_CONSTS.WOMEN_DETAILS_COLUMNS.FULL_NAME.value:f'Woman 1',
                  SQL_CONSTS.WOMEN_DETAILS_COLUMNS.PASSWORD.value: '123456',
                  SQL_CONSTS.WOMEN_DETAILS_COLUMNS.EMAIL.value:'yoni.keren@gmail.com'
                  }

requests.post(url='http://localhost:9000/register/',json=mother_details)

# for i in range(2,1000):
#
#     mother_details = {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value:f'{i}',SQL_CONSTS.WOMEN_DETAILS_COLUMNS.FULL_NAME.value:f'Woman {i}', SQL_CONSTS.WOMEN_DETAILS_COLUMNS.PASSWORD.value: '123456',
#                       SQL_CONSTS.WOMEN_DETAILS_COLUMNS.LAST_PERIOD_DATE:json.dumps(datetime(year=random.randint(2018,2022),month=random.randint(1,12),day=random.randint(1,28)),default=json_serial)}
#     requests.post(url='http://localhost:9000/register/',json=mother_details)

#
#     requests.post(url='http://localhost:9000/register/',json=mother_details)

# child={SQL_CONSTS.CHILDREN_DETAILS.IDENTIFIER.value : '1234', SQL_CONSTS.CHILDREN_DETAILS.MOTHER_ID.value:'1111'}
# requests.post(url='http://localhost:9000/save_child_details/',json=child)

# register_data = {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value:'8888',SQL_CONSTS.WOMEN_DETAILS_COLUMNS.PASSWORD.value: 'password', SQL_CONSTS.WOMEN_DETAILS_COLUMNS.FULL_NAME.value:'shira'}
# requests.post(url='http://localhost:9000/register/',json=register_data)
# login_data = {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value:'8888',SQL_CONSTS.WOMEN_DETAILS_COLUMNS.PASSWORD.value: 'password'}
# response = requests.post(url='http://localhost:9000/login/',json=login_data)
# response_str = response.content.decode()
# response_body = ast.literal_eval(response_str)
# jwt_token = response_body['access_token']
# woman_details_response = requests.get(url='http://localhost:9000/get_woman_details/8888', headers = {"Authorization":'Bearer '+jwt_token });
#print(woman_details_response)
# child={SQL_CONSTS.CHILDREN_DETAILS.IDENTIFIER.value : '1234', SQL_CONSTS.CHILDREN_DETAILS.MOTHER_ID.value:'8888'}
# response = requests.post(url='http://localhost:9000/save_child_details/',json=child, headers = {"Authorization":'Bearer '+jwt_token })
# response_str = response.content.decode()
# response_body = ast.literal_eval(response_str)
# print(response_body)
# child = requests.get(url='http://localhost:9000/get_child_details/1234', headers = {"Authorization":'Bearer '+jwt_token} );
#
# files = {'uploaded_file_key': open('b1.jpg','rb')}
#
# r = requests.post(url='http://localhost:9000/save_file/1234', files=files)

# r = requests.get(url= 'http://localhost:9000/list_files/1234')
# response_str = r.content.decode()
# response_body = ast.literal_eval(response_str)
# print(response_body)

#r = requests.get(url= 'http://localhost:9000/get_file/1234/1.pdf')



