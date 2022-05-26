import requests
from sql_consts import SQL_CONSTS


child={SQL_CONSTS.CHILDREN_DETAILS.IDENTIFIER.value : '789', SQL_CONSTS.CHILDREN_DETAILS.MOTHER_ID.value:'1234'}
requests.post(url='http://dordating.com:9000/save_child_details/5',json=child)