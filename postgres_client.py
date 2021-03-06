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

    def _update_table_by_dict(self, table_name, data, key_update_table, columns=None):
        '''
        Args:
            table_name:
            data: dictionary with keys=column names, and values=values to insert at those columns
            key_update_table:
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

        except (UniqueViolation,psycopg2.errors.NotNullViolation) as _:
            with self.conn.cursor() as cursor:
                update = f'update {table_name} set '
                update += ','.join([f' {k}=%({k})s ' for k in data.keys()])
                if key_update_table[0] == '(':  # multiple value primary key
                    if key_update_table[-1] != ')':
                        raise ValueError('Bad multiple primary key')
                    columns_names = key_update_table[1:-1].split(',')
                    primary_key_str = ','.join([f'%({column_name})s' for column_name in columns_names])
                    primary_key_str = '(' + primary_key_str + ')'
                else:
                    primary_key_str = f'%({key_update_table})s'
                update += f" where {key_update_table}={primary_key_str}"
                print(cursor.mogrify(update, data))
                cursor.execute(update, data)

    def create_women_table(self):
        '''
        CREATE TABLE women_details (identifier varchar NOT NULL,  email varchar, medical_provider_name varchar,  last_period_date  date, full_name varchar NOT NULL, num_of_pregnancy integer, birthday date, primary key (identifier));
        :return:
        '''
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"CREATE TABLE {SQL_CONSTS.TablesNames.WOMEN_DETAILS.value} ( {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value} varchar NOT NULL, "
                f" {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.EMAIL.value} varchar, {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.MEDICAL_PROVIDER_NAME.value} varchar, "
                f"{SQL_CONSTS.WOMEN_DETAILS_COLUMNS.LAST_PERIOD_DATE.value} date, {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.FULL_NAME.value} varchar NOT NULL, "
                f"{SQL_CONSTS.WOMEN_DETAILS_COLUMNS.FORGOT_PASSWORD_LINK_SECRET.value} varchar, "
                f"{SQL_CONSTS.WOMEN_DETAILS_COLUMNS.NUM_OF_PREGNENCY} integer, {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.BIRTHDAY.value} date, {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.PASSWORD.value} varchar NOT NULL , "
                f"{SQL_CONSTS.WOMEN_DETAILS_COLUMNS.ULTRASOUND_1.value} boolean default false, {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.SISI_SHELIA.value} boolean default false,"
                f"{SQL_CONSTS.WOMEN_DETAILS_COLUMNS.SHKIFUT_ORPIT.value} boolean default false, {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.SKIRAT_MARCHOT_MUKDEMET.value} boolean default false,"
                f"{SQL_CONSTS.WOMEN_DETAILS_COLUMNS.HELBON_UBARI.value} boolean default false, {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.DIKUR_MI_SHAFIR.value} boolean default false,"
                f"{SQL_CONSTS.WOMEN_DETAILS_COLUMNS.SKIRAT_MARCHOT_MEUCHERET.value} boolean default false, {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.HAMASAT_SUGARAR.value} boolean default false,"
                f"{SQL_CONSTS.WOMEN_DETAILS_COLUMNS.ULTRASOUND_2.value} boolean default false, {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.TARBIT_GBS.value} boolean default false,"
                f"{SQL_CONSTS.WOMEN_DETAILS_COLUMNS.NITUR_UBARI.value} boolean default false,"
                f"primary key({SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value}));"
            )
            return

    def save_woman_details(self, woman_details, key_update_table = SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value):
        return self._update_table_by_dict(table_name=SQL_CONSTS.TablesNames.WOMEN_DETAILS.value, data=woman_details,
                                          key_update_table=key_update_table)

    def get_woman_details(self, woman_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(
                f"select * from {SQL_CONSTS.TablesNames.WOMEN_DETAILS.value} where {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value} = %s",
                (woman_id,))
            results = cursor.fetchall()
            return results[0] if len(results) > 0 else None
    
    
    def get_woman_by_email(self,woman_email):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(
                f"select * from {SQL_CONSTS.TablesNames.WOMEN_DETAILS.value} where {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.EMAIL.value} = %s",
                (woman_email,))
            results = cursor.fetchall()
            return dict(results[0]) if len(results) > 0 else None
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
                f"{SQL_CONSTS.CHILDREN_DETAILS.CHILD_NAME.value} varchar, "
                f"{SQL_CONSTS.CHILDREN_DETAILS.BIRTHDAY.value} date, "
                f"{SQL_CONSTS.CHILDREN_DETAILS.MOTHER_ID.value} varchar, {SQL_CONSTS.CHILDREN_DETAILS.PALETZET_MANA_1.value} boolean default false,"
                f"{SQL_CONSTS.CHILDREN_DETAILS.PALETZET_MANA_2.value} boolean default false, {SQL_CONSTS.CHILDREN_DETAILS.PALETZET_MANA_3.value} boolean default false,"
                f"{SQL_CONSTS.CHILDREN_DETAILS.PALETZET_MANA_4.value} boolean default false, {SQL_CONSTS.CHILDREN_DETAILS.POLIO_1.value} boolean default false,"
                f"{SQL_CONSTS.CHILDREN_DETAILS.POLIO_2.value} boolean default false, {SQL_CONSTS.CHILDREN_DETAILS.HEMOFILOS_MANA_1.value} boolean default false,"
                f"{SQL_CONSTS.CHILDREN_DETAILS.HEMOFILOS_MANA_2.value} boolean default false, {SQL_CONSTS.CHILDREN_DETAILS.HEMOFILOS_MANA_3.value} boolean default false,"
                f"{SQL_CONSTS.CHILDREN_DETAILS.HEMOFILOS_MANA_4.value} boolean default false, {SQL_CONSTS.CHILDREN_DETAILS.PNOIMOKOK_MANA_1.value} boolean default false,"
                f"{SQL_CONSTS.CHILDREN_DETAILS.PNOIMOKOK_MANA_2.value} boolean default false, {SQL_CONSTS.CHILDREN_DETAILS.PNOIMOKOK_MANA_3.value} boolean default false,"
                f"{SQL_CONSTS.CHILDREN_DETAILS.NEGIF_ROTA_MANA_1.value} boolean default false,"
                f"{SQL_CONSTS.CHILDREN_DETAILS.NEGIF_ROTA_MANA_2.value} boolean default false, {SQL_CONSTS.CHILDREN_DETAILS.NEGIF_ROTA_MANA_3.value} boolean default false,"
                f"{SQL_CONSTS.CHILDREN_DETAILS.HATZEVET_HAZERET_ADEMET_HABABUOT.value} boolean default false, {SQL_CONSTS.CHILDREN_DETAILS.TZHEVET_A_MANA_1.value} boolean default false,"
                f"{SQL_CONSTS.CHILDREN_DETAILS.TZHEVET_A_MANA_2.value} boolean default false,"
                f" FOREIGN KEY({SQL_CONSTS.CHILDREN_DETAILS.MOTHER_ID.value}) REFERENCES {SQL_CONSTS.TablesNames.WOMEN_DETAILS.value}({SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value}) , "
                f"primary key({SQL_CONSTS.CHILDREN_DETAILS.IDENTIFIER.value}));"
            )
            return

    def add_child(self, child_details):
        return self._update_table_by_dict(table_name=SQL_CONSTS.TablesNames.CHILD_DETAILS.value, data=child_details,
                                          key_update_table=SQL_CONSTS.CHILDREN_DETAILS.IDENTIFIER.value)

    def get_child_details(self, child_id):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(
                f"select * from {SQL_CONSTS.TablesNames.CHILD_DETAILS.value} where {SQL_CONSTS.CHILDREN_DETAILS.IDENTIFIER.value} = %s",
                (child_id,))
            
            results = cursor.fetchall()
            return results[0] if len(results) > 0 else None
        
    def get_women_by_days_from_last_period(self,days_from_last_period):
        '''
        Original sample query:
        select * from women_details where date_trunc('day','now'::timestamp - last_period_date)< interval '100 day'
        :return:
        '''

        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(
               f"select * from women_details where date_trunc('day', 'now'::timestamp - {SQL_CONSTS.WOMEN_DETAILS_COLUMNS.LAST_PERIOD_DATE.value}) = interval '%s day'"
                ,(days_from_last_period,))
    
            results = cursor.fetchall()
            return [dict(x) for x in results]
        
    def get_children_by_days_from_birthday(self,days_from_birthday):
        """Original query:
        select * from children_details join women_details on mother_id=women_details.identifier where date_trunc('day','now'::timestamp - children_details.birthday)< interval '20 day'
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(
                f"select * from {SQL_CONSTS.TablesNames.CHILD_DETAILS.value} join {SQL_CONSTS.TablesNames.WOMEN_DETAILS.value} on {SQL_CONSTS.CHILDREN_DETAILS.MOTHER_ID.value}={SQL_CONSTS.TablesNames.WOMEN_DETAILS.value}.{SQL_CONSTS.WOMEN_DETAILS_COLUMNS.IDENTIFIER.value} "
                f" where date_trunc('day','now'::timestamp - {SQL_CONSTS.TablesNames.CHILD_DETAILS.value}.{SQL_CONSTS.CHILDREN_DETAILS.BIRTHDAY.value})< interval '%s day'"
                , (days_from_birthday,))
    
            results = cursor.fetchall()
            return [dict(x) for x in results]