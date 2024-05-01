from src.db.manager import BaseManager
from .types import Integer, Float, BaseType, String, Text, Boolean
import inspect
from .meta import MetaField
from .connection import db_connect

class MetaModel(type):
    manager_class = BaseManager

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()



RESERVED_WORDS = ["def"]

class BaseModel(metaclass=MetaModel):
    __table_name__: str = "" # the table where this entity belongs to
    __exist__ = False
    __old__ = {}
    id = None

    def __init__(self, **row_data):
        self._meta = self._get_meta()
        self.__old__ = row_data
        # make sure field name match with sql code
        for field_name, value in row_data.items():
            if field_name in RESERVED_WORDS:
                # if field is a reseved word in python, field name must end with underscore
                field_name = field_name + "_"
            field = getattr(self, field_name)
            if isinstance(field, Integer):
                setattr(self, field_name, int(value))
            elif isinstance(field, Float):
                setattr(self, field_name, float(value))
            elif isinstance(field, String):
                setattr(self, field_name, str(value))
            elif isinstance(field, Text):
                setattr(self, field_name, str(value))
            elif isinstance(field, Boolean):
                setattr(self, field_name, bool(value))
            else:
                setattr(self, field_name, value)

    def _get_meta(self):
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        fields = [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
        fields = dict(fields)
        meta_fields = []
        for field_name, value in fields.items():
            field_value = getattr(self, field_name)
            if isinstance(field_value, BaseType):
                meta_fields.append(field_name)
        return MetaField(self, meta_fields)

    def __repr__(self):
        attrs_format = ", ".join([f'{field}={value}' for field, value in self.__dict__.items()])
        return f"<{self.__class__.__name__}: ({attrs_format})>"
    
    def update(self, *update_fields):
        """
        Update a record in database
        
        If update fields param is provided, only the field specified in that param will be use to update
        """
        connection = db_connect()
        cursor = connection.cursor()
        self.on_update()

        if update_fields: # if update field exist
            attr_update = {}
            for update_field in update_fields:
                update_field_value = getattr(self, update_field)
                if update_field[-1] == "_":  # if last character in field ends with underscore
                    # showing this field is a reserved keyword
                    update_field = update_field[:-1]
                attr_update[update_field] = update_field_value
            
            
            query_placeholders = ', '.join([field+'=%s' for field, value in attr_update.items()])
            sql = 'UPDATE %s SET %s WHERE id = %s' % (self.__table_name__, query_placeholders, self.id)
            vals = tuple([value for field, value in attr_update.items()])
            cursor.execute(sql, vals)
            connection.commit()
            cursor.close()
            connection.close()
            
        else:
            attrs_format = ", ".join([f'{field}={value}' for field, value in self.attributes.items()])
            query_placeholders = ', '.join([field+'=%s' for field, value in self.attributes.items()])
            sql = 'UPDATE %s SET %s WHERE id = %s' % (self.__table_name__, query_placeholders, self.id)
            cursor.execute(sql, tuple([str(val) for val in self._meta.values]))
            
            connection.commit()
            cursor.close()
            connection.close()
    
    def on_update(self):
        """This function will get called every changes to this database record"""
        pass
    
    def on_create(self):
        """This function will get called when creating new database record"""
        pass
    
    @property
    def attributes(self):
        return dict(zip(self._meta.fields, self._meta.values))
    
    def to_dict(self):
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        fields = [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
        fields = dict(fields[1:])
        return fields
    
    def save(self, *update_fields):
        """
        create or update a record in database
        
        if parameter update_fields is pass, it will only effect update function
        the update fields parameter ensure only that particular field gets updated
        """
        connection = db_connect()
        cursor = connection.cursor()
        if self.id: # id exists means record exists
            self.on_update() # call update hook
            return self.update(*update_fields)
        
        self.on_create() # call create hook

        query_placeholders = ', '.join(['%s'] * len(self._meta.fields))
        query_columns = ', '.join(self._meta.fields)
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.__table_name__, query_columns, query_placeholders)
        values = tuple([str(val) for val in self._meta.values])

        cursor.execute(sql, values)
        connection.commit()
        cursor.close()
        connection.close()
    
    def delete(self):
        connection = db_connect()
        cursor = connection.cursor()
        sql = 'DELETE FROM ' + self.__table_name__ + " WHERE id = %s"
        cursor.execute(sql, (self.id, ))
        connection.commit()
        self.id = None
        cursor.close()
        connection.close()
    
    def raw_insert(self, sql, val):
        connection = db_connect()
        
        cursor = connection.cursor()

        cursor.execute(sql, val)
        connection.commit()

        cursor.close()
        connection.close()
    
    def is_dirty(self, *fields):
        """
        Return true if value of fields are changed
        """
        if fields:
            for field in fields:
                if self.__old__.get(field) != field:
                    return True
            return False