import unittest

from .model import BaseModel
from .types import Integer, String

class Item(BaseModel):
    __table_name__ = "test_table"

    ID = Integer()
    Name = String()

class TestModelSelectQuery(unittest.TestCase):
    def test_select_all_with_id(self):
        smt = Item.objects.select().where(id=10)
        q = smt.sql_query()
        self.assertEqual("SELECT * FROM test_table WHERE id = %s", q)

        # should have first params being 10
        params = smt.sql_params()
        self.assertEqual(10, params[0])
    
    def test_select_name_by_id(self):
        smt = Item.objects.select("name").where(id=10)
        q = smt.sql_query()
        # should automatically inject id
        self.assertEqual("SELECT id, name FROM test_table WHERE id = %s", q)

        # should have first params being 10
        params = smt.sql_params()
        self.assertEqual(10, params[0])

if __name__ == '__main__':
    unittest.main()