import unittest

from prog.mem_nr_db import Query, QueryLogic, MemNRDB, Table, DBException, Row, DBTypeError


class TestDB(unittest.TestCase):

    def test_filter_comp(self):
        Q = Query("table_name")
        q = Q.test == 10  # type: Query
        self.assertIsInstance(q, Query)

        def test_q(check_func):
            self.assertTrue(check_func({"test": 10}))
            self.assertFalse(check_func({"test": 15}))
            self.assertFalse(check_func({"test": None}))
            self.assertTrue(check_func({"test": 10.}))
            self.assertFalse(check_func({"test": []}))
            self.assertFalse(check_func({"test": "10"}))
            self.assertFalse(check_func({"test": True}))
            self.assertFalse(check_func({12: 10}))
            self.assertFalse(check_func({"test_test": 10}))
            self.assertFalse(check_func({}))

        test_q(q._check)

        q = Query("table_name")[12] == True  # type: Query
        self.assertIsInstance(q, Query)
        ch = q._check

        self.assertTrue(ch({12: True}))
        self.assertFalse(ch({12: 10}))
        self.assertFalse(ch({12: 15}))
        self.assertFalse(ch({12: None}))
        self.assertFalse(ch({12: 10.}))
        self.assertFalse(ch({12: []}))
        self.assertFalse(ch({12: False}))
        self.assertFalse(ch({12: "10"}))
        self.assertFalse(ch({12: 10}))
        self.assertFalse(ch({"12": True}))
        self.assertFalse(ch({}))

        q = Query("table_name").a < 10  # type: Query
        self.assertIsInstance(q, Query)
        ch = q._check

        self.assertTrue(ch({"a": 5}))
        self.assertFalse(ch({"a": 10}))
        self.assertFalse(ch({"a": 15}))

        q = Query("__").field.exist()
        self.assertIsInstance(q, Query)

        ch = q._check

        self.assertTrue(ch({"field": 123}))
        self.assertTrue(ch({"field": []}))
        self.assertFalse(ch({"field": None}))
        self.assertFalse(ch({}))
        self.assertFalse(ch({"piu": 123}))
        self.assertFalse(ch({'cost': {'group_nsu24': 0.8},
                                      'faculty': 0,
                                      'faculty_name': '',
                                      'first_name': 'Наталья',
                                      'graduation': 0,
                                      'id': 273855550,
                                      'last_name': 'Иванцова',
                                      'sex': 1,
                                      'universities': [],
                                      'university': 0,
                                      'university_name': ''}))

    def test_convert(self):
        t = Table("tn", convert=True)
        row = t.insert({"int": "123",
                        "float": "123.444",
                        "str": "test",
                        "int_": 123,
                        "float_": 123.444})
        self.assertEqual(row["int"],  123)
        self.assertEqual(row["float"],  123.444)
        self.assertEqual(row["str"],  "test")
        self.assertEqual(row["int_"],  123)
        self.assertEqual(row["float_"],  123.444)

        t = Table("tn", convert=True, convert_exclude=['exclude1', "exclude2"])
        row = t.insert({"int": "123",
                        "float": "123.444",
                        "str": "test",
                        "int_": 123,
                        "float_": 123.444,
                        "exclude1": "123.33",
                        "exclude2": "123"})
        self.assertEqual(row["int"], 123)
        self.assertEqual(row["float"], 123.444)
        self.assertEqual(row["str"], "test")
        self.assertEqual(row["int_"], 123)
        self.assertEqual(row["float_"], 123.444)
        self.assertEqual(row["exclude1"], "123.33")
        self.assertEqual(row["exclude2"], "123")


    def test_filter_logic(self):
        q = (Query("table").a < 10) & (Query("table").b >= 20)  # type: QueryLogic
        self.assertIsInstance(q, QueryLogic)
        ch = q._check

        self.assertTrue(ch({"a": 0, "b": 30}))
        self.assertFalse(ch({"a": 0, "b": 10}))
        self.assertFalse(ch({"a": 20, "b": 30}))
        self.assertFalse(ch({"a": 20, "b": 10}))
        self.assertTrue(ch({"a": 0, "b": 20}))

        self.assertFalse(ch({"b": 30}))
        self.assertFalse(ch({"a": 0}))
        self.assertFalse(ch({}))
        self.assertFalse(ch({"a": 0, "b": None}))

        q = (Query("table").a < 10) | (Query("table").b >= 20)  # type: QueryLogic
        self.assertIsInstance(q, QueryLogic)
        ch = q._check

        self.assertTrue(ch({"a": 0, "b": 30}))
        self.assertTrue(ch({"a": 0, "b": 10}))
        self.assertTrue(ch({"a": 20, "b": 30}))
        self.assertFalse(ch({"a": 20, "b": 10}))
        self.assertTrue(ch({"a": 0, "b": 20}))

        self.assertTrue(ch({"b": 30}))
        self.assertTrue(ch({"a": 0}))
        self.assertFalse(ch({}))
        self.assertTrue(ch({"a": 0, "b": None}))

    def test_db_query(self):
        db = MemNRDB()
        db.init_table("test")
        self.assertIsInstance(db['test'], Table)

        with self.assertRaises(DBException):
            t = db['tost']

        t = db['test']
        t.insert({"a": 5, "b": 10})
        t.insert({"a": 10, "b": 10})
        t.insert({"a": 20, "b": 10})
        t.insert({"a": 5, "b": 20})
        t.insert({"a": 10, "b": 20})
        t.insert({"a": 20, "b": 20})
        t.insert({"a": 5, "b": 25})
        t.insert({"a": 10, "b": 25})
        t.insert({"a": 20, "b": 25})
        t.insert({"a": 20})
        t.insert({"b": 20})
        t.insert({})

        q = (Query("test").a < 15) & (Query("test").b > 15)

        data = list(db.query(q).all())
        self.assertEqual(len(data), 4)
        for r in data:
            self.assertTrue((r['a'] < 15) and (r['b'] > 15))

        data_l = list(db.query(q).limit(2))
        self.assertEqual(len(data_l), 2)

        data_l = list(db.query(q).limit(5))
        self.assertEqual(len(data_l), 4)

        with self.assertRaises(DBException):
            q = db.query(Query("tost").field < 10)
            list(q.all())

    def test_db_index(self):
        db = MemNRDB()
        db.init_table("tost")

        t = db['tost']
        row2 = t.insert({"id": 2})
        row1 = t.insert({"hello": "world"})
        row3 = t.insert({"world": "hello"})

        self.assertEqual(row1['id'], 1)
        self.assertEqual(row2['id'], 2)
        self.assertEqual(row3['id'], 3)

        with self.assertRaises(DBException):
            t.insert({"id": 3})

    def test_insert_update(self):
        db = MemNRDB()
        db.init_table("tost")

        t = db['tost']
        t.insert({"id": 2})
        t.insert({"hello": "world", "zzz": "xxx"})
        t.insert({"world": "hello"})
        with self.assertRaises(DBException):
            t.insert({"id": None, 'c': 4})

        with self.assertRaises(DBException):
            t.update({"id": 4, "val": 123, "prev_val": 456})

        t.update({"id": 1, "hello": "WORLD", "xxx": "zzz"})
        row = t.get(1)
        self.assertEqual(row['id'], 1)
        self.assertEqual(row['hello'], "WORLD")
        self.assertEqual(row['zzz'], "xxx")
        self.assertEqual(row['xxx'], "zzz")

        row = t.update({"id": 1, "xxx": None})
        self.assertEqual("xxx" not in row, True)
        self.assertEqual(row['zzz'], "xxx")

        with self.assertRaises(DBException):
            t.update({"id": None, "yyY": 123})

        t.get(3)['prev_val'] = 456

        t.ins_upd({"id": 3, "val": 321})
        t.ins_upd({"id": 98, "value": 12345})

        row = t.get(3)
        self.assertEqual(row['val'], 321)
        self.assertEqual(row['prev_val'], 456)

        row98 = t.get(98)
        self.assertEqual(row98['value'], 12345)

    def test_row(self):
        db = MemNRDB()
        db.init_table("tost")

        t = db['tost']
        t.insert({
            "id": 2,
            "test": "value",
            (1, 2): (3, 4),
            12: 34
        })

        row = t.get(2, to_class=True)
        self.assertIsInstance(row, Row)
        self.assertEqual(row.id, 2)
        self.assertEqual(row.test, "value")
        self.assertEqual(row[12], 34)
        self.assertEqual(row[1, 2], (3, 4))
        self.assertIsInstance(row._raw_data, dict)
        self.assertIsNone(row.non_exist)
        with self.assertRaises(KeyError):
            val = row['now_exist']

        row.unk = 12
        self.assertEqual(row.unk, 12)
        self.assertEqual(row['unk'], 12)
        row['unk'] = 15
        row['unk1'] = 16
        self.assertEqual(row.unk, 15)
        self.assertEqual(row['unk'], 15)
        self.assertEqual(row.unk1, 16)
        self.assertEqual(row['unk1'], 16)

    def test_assert(self):
        db = MemNRDB()
        db.init_table("tost")

        t = db['tost']
        with self.assertRaises(DBTypeError):
            t.insert([])

    def test_serialize(self):
        db = MemNRDB()
        t = db.init_table("tost", convert=False)

        t.insert({"a": 12})
        t.insert({"бля": 23})

        tt = db.init_table("test")

        tt.insert({"c": 34})
        tt.insert({"d": 45})

        tc = db.init_table("test_cnv", convert=True, convert_exclude=['a', 'b'])

        db.serialize("test_file.json")

        new_db = MemNRDB.load("test_file.json")

        tt = new_db['test']
        t = new_db['tost']
        tc = new_db['test_cnv']

        self.assertIsInstance(tt, Table)
        self.assertIsInstance(t, Table)
        self.assertEqual(tc.convert_exclude, ['a', 'b'])
        self.assertEqual(tc.convert, True)

        r = t.get(1, to_class=True)
        r2 = t.get(2, to_class=True)

        rr = tt.get(2, to_class=True)

        self.assertEqual(r.a, 12)
        self.assertEqual(r2['бля'], 23)

        self.assertEqual(rr.d, 45)

        r3 = Row(t.insert({"test": 333}))

        self.assertEqual(r3.test, 333)


if __name__ == '__main__':
    unittest.main()
