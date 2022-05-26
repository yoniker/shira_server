from sql_consts import SQL_CONSTS
import psycopg2
from psycopg2.errors import UniqueViolation
import psycopg2.extras
class PostTBD:
    
    
    def __init__(self):
        connect_str = "dbname='shira' user='yoni' host='localhost' " + \
                      "password='dor'"
        self.conn = psycopg2.connect(connect_str)
        self.conn.autocommit = True

    def _update_table_by_dict(self, table_name, data, primary_key, columns=None):
        '''

        Args:
            table_name:
            data: dictionary with keys=column names, and values=values to insert at those columns
            primary_key:
            columns: a columns enum str mixin class for which we can check that the data has the keys that we expect

        Returns:

        '''
        if columns is not None:
            if not all([k in [column.value for column in columns] for k in data.keys()]):
                raise ValueError('There are columns')
        if type(data) != dict: raise ValueError(f'Error inserting into table,Expecting a dictionary, got {type(data)}')
        keys = data.keys()
        columns = ','.join(keys)
        values = ','.join(['%({})s'.format(k) for k in keys])
        insert = 'insert into {0} ({1}) values ({2})'.format(table_name, columns, values)
        try:
            with self.conn.cursor() as cursor:
                print(cursor.mogrify(insert, data))
                cursor.execute(insert, data)
    
        except UniqueViolation as _:
            with self.conn.cursor() as cursor:
                update = f'update {table_name} set '
                update += ','.join([f' {k}=%({k})s ' for k in data.keys()])
                if primary_key[0] == '(':  # multiple value primary key
                    if primary_key[-1] != ')':
                        raise ValueError('Bad multiple primary key')
                    columns_names = primary_key[1:-1].split(',')
                    primary_key_str = ','.join([f'%({column_name})s' for column_name in columns_names])
                    primary_key_str = '(' + primary_key_str + ')'
                else:
                    primary_key_str = f'%({primary_key})s'
                update += f" where {primary_key}={primary_key_str}"
                print(cursor.mogrify(update, data))
                cursor.execute(update, data)
    
    def create_women_table(self):
        '''
        
        CREATE TABLE women (identifier varchar NOT NULL,  email varchar, medical_provider_name varchar,  last_period_date  date, full_name varchar NOT NULL, num_of_pregnancy integer, birthday date, primary key (identifier));
        :return:
        '''
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"CREATE TABLE {SQL_CONSTS.TablesNames.WOMEN_DETAILS.value} ( {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value} varchar NOT NULL, "
                f" {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.EMAIL.value} varchar, {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.MEDICAL_PROVIDER_NAME.value} varchar, "
                f"{SQL_CONSTS.WOMEN_DETAILS_COLUMNS.LAST_PERIOD_DATE.value} date, {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.FULL_NAME.value} varchar NOT NULL, "
            f"{SQL_CONSTS.WOMEN_DETAILS_COLUMNS.NUM_OF_PREGNENCY} integer, {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.BIRTHDAY.value} date, "
            f"primary key({SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value}));"
            )
            return
        
    def add_woman(self,woman_details):
        return self._update_table_by_dict(table_name=SQL_CONSTS.TablesNames.WOMEN_DETAILS.value,data = woman_details, primary_key=SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value)
    
    def get_woman_details(self,woman_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(f"select * from {SQL_CONSTS.TablesNames.WOMEN_DETAILS.value} where {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value} = %s", (woman_id,))
            results = cursor.fetchall()
            return results[0] if len(results)>0 else None

    '''create children table sql'''

    def create_child_table(self):
    
        '''
        CREATE TABLE child (identifier varchar NOT NULL, full_name varchar, birthday date, primary key (identifier));
        :param self:
        :return:
        '''
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"CREATE TABLE {SQL_CONSTS.TablesNames.CHILD_DETAILS.value} ( {SQL_CONSTS.CHILDREN_DETAILS.IDENTIFIER.value} varchar NOT NULL, "
                f"{SQL_CONSTS.CHILDREN_DETAILS.FULL_NAME.value} varchar, "
                f"{SQL_CONSTS.CHILDREN_DETAILS.BIRTHDAY.value} date, "
                f"{SQL_CONSTS.CHILDREN_DETAILS.MOTHER_ID.value} varchar,"
                f" FOREIGN KEY({SQL_CONSTS.CHILDREN_DETAILS.MOTHER_ID.value}) REFERENCES {SQL_CONSTS.TablesNames.WOMEN_DETAILS.value}({SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value}) , "
                f"primary key({SQL_CONSTS.CHILDREN_DETAILS.IDENTIFIER.value}));"
            )
            return

    def add_child(self, child_details):
        return self._update_table_by_dict(table_name=SQL_CONSTS.TablesNames.CHILD_DETAILS.value, data=child_details,
                                          primary_key=SQL_CONSTS.CHILDREN_DETAILS.IDENTIFIER.value)

    def get_child_details(self, child_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(
                f"select * from {SQL_CONSTS.TablesNames.CHILD_DETAILS.value} where {SQL_CONSTS.CHILDREN_DETAILS.IDENTIFIER.value} = %s",
                (child_id,))
            results = cursor.fetchall()
            return results[0] if len(results) > 0 else None
    
    
    
