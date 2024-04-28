from .constant import *
from .connection import db_connect

class QueryCondition:
    @staticmethod 
    def greater_than(value):
        return ('>', value)
    
    @staticmethod 
    def less_than(value):
        return ('<', value)
    
    @staticmethod 
    def greater_than_or_equal(value):
        return ('>=', value)
    
    @staticmethod 
    def less_than_or_equal(value):
        return ('<=', value)
    
    @staticmethod 
    def like(value):
        return ('LIKE', "%" + value + "%")
    
    @staticmethod 
    def null(value):
        if value:
            return ('IS NULL', None)
        else:
            return ('IS NOT NULL', None)

CONDITIONS = {
    "__lt": QueryCondition.less_than,
    "__gt": QueryCondition.greater_than,
    "__lte": QueryCondition.less_than_or_equal,
    "__gte": QueryCondition.greater_than_or_equal,
    "__contains": QueryCondition.like,
    "__null": QueryCondition.null
}

RESERVED_KEYWORDS = ["range"]

class BaseManager:
    def __init__(self, model_class):
        self.model_class = model_class
        self.sql: str = ''
        self.data = []
        self.order_sql = ''
    
    def set_connection(self):
        connection = db_connect()
        return connection
    
    def _get_cursor(self, connection):
        return connection.cursor()

    def select(self, *field_names, chunk_size=2000):
        """
        TODO chunk_size
        """
        if field_names:
            fields_format = ', '.join(field_names)
            query = f"SELECT id, {fields_format} FROM {self.model_class.__table_name__}"
        else:
            query = f"SELECT * FROM {self.model_class.__table_name__}"
        self.sql = query
        return self
    
    def sql_query(self) -> str:
        """
        return final sql string
        """
        query = self.sql
        if self.order_sql:
            query = self.sql + ' ' + self.order_sql
        return query
    
    def sql_params(self) -> list:
        return self.data

    def fetch_all(self):
        """Fetch all result found"""
        connection = self.set_connection()
        cursor = self._get_cursor(connection)
        if self.order_sql:
            self.sql = self.sql + ' ' + self.order_sql
        if self.data:
            cursor.execute(self.sql, tuple([str(val) for val in self.data]))
        else:
            cursor.execute(self.sql)
        model_objects = list()
        result = cursor.fetchall()
        field_names = [i[0] for i in cursor.description]
        for row_values in result:
            keys, values = field_names, row_values
            row_data = dict(zip(keys, values))
            model = self.model_class(**row_data)
            model.__exist__ = True
            model_objects.append(model)
        connection.close()
        return model_objects
    
    def fetch_one(self):
        """Fetch first result found. Return None if there is none"""
        connection = self.set_connection()
        cursor = self._get_cursor(connection)
        if self.order_sql:
            self.sql = self.sql + ' ' + self.order_sql
        
        if self.data:
            cursor.execute(self.sql, tuple([str(val) for val in self.data]))
        else:
            cursor.execute(self.sql)
        model_objects = {}
        result = cursor.fetchone()
        if not result:
            return None
        field_names = [i[0] for i in cursor.description]
        row_data = dict(zip(field_names, result))
        model = self.model_class(**row_data)
        model.__exist__ = True
        model_objects = model
        connection.close()
        return model_objects

    def _get_where_condition(self, key: str, value: str):
        """
        get where condition
        """
        if key.lower() in RESERVED_KEYWORDS:
            key = f"`{key}`"
        for cond_key, cond_func in CONDITIONS.items():
            if key.endswith(cond_key):
                query_cond_key, query_cond_value = cond_func(value)
                key = key.replace(cond_key, " ")
                if query_cond_value != None:
                    self.data.append(query_cond_value)
                    return key + " "+ query_cond_key +" " + "%s"
                return key + " "+ query_cond_key +" "

        self.data.append(value)
        return key + " = %s"

    def where(self, **query):
        key_word = " AND " if " WHERE " in self.sql else " WHERE "
        where_condition = ""
        for key, value in query.items():
            if key == list(query)[-1]: # last key in query
                condition = self._get_where_condition(key, value)
            else:
                condition = self._get_where_condition(key, value) + " AND "# add AND condition if there are more keys
            where_condition = where_condition + condition
        self.sql = self.sql + key_word + where_condition
        return self
    
    def filter(self, **query):
        self.sql = f"SELECT * FROM {self.model_class.__table_name__}"
        return self.where(**query)

    def bulk_create(self, rows: list):
        pass
    
    def order_by(self, *column):
        sql = 'ORDER BY '
        data = []
        for col in column:
            order_type = 'ASC'
            if col.endswith('__desc'):
                col = col.replace('__desc', ' ')
                order_type = 'DESC'
            elif col.endswith('__asc'):
                col = col.replace('__asc', ' ')
                order_type = 'ASC'
            data.append(col + ' ' + order_type)
        self.order_sql = sql + ', '.join(data)
        return self

    def update(self, new_data: dict) -> None:
        """
        TODO
        """
        pass

    def raw_sql(self, query, args=(), one=False) -> dict:
        """
        Execute raw SQL provided with arguments
        
        query: String
        args: Tuple
        if @param one is True this will return single JSON object
        return: dictionary
        Example: raw_sql("select * from user where name = %s", ('smith'))
        """
        connection = self.set_connection()
        cursor = self._get_cursor(connection)
        cursor.execute(query, args)
        r = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]
        cursor.close()
        connection.close()
        return (r[0] if r else None) if one else r