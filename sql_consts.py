from enum import Enum
class SQL_CONSTS:
    class TablesNames(str, Enum):
        WOMEN_DETAILS = 'women_details'
        CHILD_DETAILS = 'children_details'
        
    class WOMEN_DETAILS_COLUMNS(str, Enum):
        IDENTIFIER = 'identifier'
        EMAIL ='email'
        MEDICAL_PROVIDER_NAME = 'medical_provider_name'
        LAST_PERIOD_DATE ='last_period_date'
        FULL_NAME = 'full_name'
        NUM_OF_PREGNENCY = 'num_of_pregnancy'
        BIRTHDAY = 'birthday'
        PRIMARY_KEY = f'{IDENTIFIER}'

    class CHILDREN_DETAILS(str, Enum):
        IDENTIFIER = 'identifier'
        MOTHER_ID = 'mother_id'
        FULL_NAME = 'full_name'
        BIRTHDAY = 'birthday'
        PRIMARY_KEY = f'{IDENTIFIER}'
    
    
