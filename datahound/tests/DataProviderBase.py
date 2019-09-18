import unittest
import warnings

from datahound import DataProviderBase


class DataProvider(DataProviderBase):
    db_path = 'db/tests.sqlite3'

    def __init__(self):
        super().__init__(DataProvider.db_path)

    def __del__(self):
        self.db_path = None


class FalseProvider(DataProviderBase):
    db_path = 'db/error_db.txt'

    def __init__(self):
        super().__init__(FalseProvider.db_path)

    def __del__(self):
        self.db_path = None


class Helper(object):
    @staticmethod
    def setup():
        dataProvider = DataProvider()
        sql = 'create table if not exists test (' \
            'id integer not null primary key autoincrement, ' \
            'name varchar(32) not null)'
        dataProvider.execute(sql)

    @staticmethod
    def cleanup():
        dataProvider = DataProvider()
        sql = 'drop table test'
        dataProvider.execute(sql)

    @staticmethod
    def truncateTable(table):
        dataProvider = DataProvider()
        sql = 'delete from {}'.format(table)
        dataProvider.execute(sql)

class DataProviderBaseTest(unittest.TestCase):
    def test_connection_error(self):
        sql = 'select * from test'
        provider = FalseProvider()
        self.assertRaises(Exception, lambda: provider.execute(sql))

    def test_executeCreate(self):
        Helper.setup()
        dataProvider = DataProvider()

        sql = "select name from sqlite_master where type='table' and name='test'"
        actual = dataProvider.fetchall(sql)
        self.assertGreater(len(actual), 0)

    def test_executeInsertTruncate(self):
        Helper.truncateTable('test')
        sql = "insert into test (name) values ('datatest1')"
        dataProvider = DataProvider()
        dataProvider.execute(sql)

        actual_sql = 'select * from test'
        actual = dataProvider.fetchall(actual_sql)
        self.assertGreater(len(actual), 0)
        self.assertEqual(actual[0][1], 'datatest1')
        Helper.truncateTable('test')
        cleaned = dataProvider.fetchall(actual_sql)
        self.assertEqual(len(cleaned), 0)

    def test_fetchall(self):
        Helper.truncateTable('test')
        sql = "insert into test (name) values ('booger'), ('testing')"
        dataProvider = DataProvider()
        dataProvider.execute(sql)

        actual_sql = 'select * from test'
        actual = dataProvider.fetchall(actual_sql)
        self.assertEqual(len(actual), 2)
        Helper.truncateTable('test')
        self.assertEqual(len(dataProvider.fetchall(actual_sql)), 0)

    def test_fetchmany(self):
        sql = "insert into test (name) values ('boogers'), ('boogers1'), ('boogers3'), ('boogers4')"
        dataProvider = DataProvider()
        dataProvider.execute(sql)

        actual_sql = "select * from test where name like '%boogers%'"
        actual = dataProvider.fetchmany(3, actual_sql)
        self.assertEqual(len(actual), 3)
        Helper.truncateTable('test')

    def test_fetchone(self):
        sql = "insert into test (name) values ('fetchone')"
        dataProvider = DataProvider()
        dataProvider.execute(sql)

        actual_sql = 'select * from test limit 1'
        actual = dataProvider.fetchone(actual_sql)
        self.assertIsNotNone(actual)
        Helper.truncateTable('test')
        self.assertIsNone(dataProvider.fetchone(actual_sql))

    def test_execute_scripts(self):
        sql = "create table if not exists testing (id integer not null primary key autoincrement, name varchar(64)" \
              " not null); insert into testing (name) values ('testing1'), ('testing2')"
        dataProvider = DataProvider()
        dataProvider.execute_scripts(sql)

        actual_sql = 'select * from testing'
        actual = dataProvider.fetchall(actual_sql)
        self.assertIsNotNone(actual)
        self.assertEqual(len(actual), 2)
        dataProvider.execute('drop table testing')

    def test_execute_scripts_fail(self):
        sql = "create table if not exists testing (id integer not null primary key autoincrement, name varchar(64)" \
              "not null)"
        dataProvider = DataProvider()
        self.assertRaises(Exception, lambda: dataProvider.execute_scripts(sql))

    def test_fetchallwithparameters(self):
        dataProvider = DataProvider()
        sql = 'insert into test (name) values (?), (?)'
        dataProvider.execute(sql, 'test1', 'test2')

        actual_sql = 'select name from test where name = ?'
        actual = dataProvider.fetchall(actual_sql, 'test1')
        self.assertEqual(len(actual), 1)
        self.assertEqual([('test1',)], actual)
        Helper.truncateTable('test')

    def test_executereturnid(self):
        dataProvider = DataProvider()
        sql = 'insert into test (name) values (?)'
        last_id = dataProvider.execute_return_id(sql, 'testing')

        self.assertTrue(type(last_id) == int)
        Helper.truncateTable('test')

    def test_executereturnid_deprecation(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter('always')

            dataProvider = DataProvider()
            sql = 'insert into test (name) values (?)'
            dataProvider.execute_return_id(sql, 'testing')

            self.assertTrue(len(warning) == 1)
            self.assertTrue(issubclass(warning[-1].category, DeprecationWarning))
            self.assertTrue('This method is deprecated. It will be removed in an upcoming version. Please use "insert_return_id" instead.'\
                   in str(warning[-1].message))

    def test_insertreturnid(self):
        dataProvider = DataProvider()
        sql = 'insert into test (name) values (?)'
        last_id = dataProvider.insert_return_id(sql, 'testing')

        self.assertTrue(type(last_id) == int)
        Helper.truncateTable('test')

    def test_insertreturnid_fail(self):
        dataProvider = DataProvider()
        sql = "update test set name = 'test' where id = 1"

        self.assertRaises(Exception, lambda: dataProvider.insert_return_id(sql))

    def test_insertmany(self):
        dataProvider = DataProvider()
        sql = 'INSERT INTO test (name) VALUES (?)'
        parameters = ('Test1',), ('Test2',), ('Test3',)
        dataProvider.insert_many(sql, *parameters)

        sql = 'SELECT name FROM test WHERE name IN (\'Test1\', \'Test2\', \'Test3\')'
        records = dataProvider.fetchall(sql)

        for record in records:
            self.assertTrue(record in parameters)

        Helper.truncateTable('test')

    def test_insertmany_fail(self):
        dataProvider = DataProvider()
        sql = 'UPDATE test SET name = \'Testing\' WHERE id = 0'
        parameters = ('Test1',), ('Test2',), ('Test3',)

        self.assertRaises(Exception, lambda: dataProvider.insert_many(sql, *parameters))
