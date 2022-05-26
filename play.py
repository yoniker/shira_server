from postgres_client import PostTBD
from sql_consts import SQL_CONSTS
client=PostTBD()
client.add_child({SQL_CONSTS.CHILDREN_DETAILS.IDENTIFIER.value : '456', SQL_CONSTS.CHILDREN_DETAILS.MOTHER_ID.value:'555'} )