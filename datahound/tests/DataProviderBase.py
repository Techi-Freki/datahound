import unittest
import warnings
import os

from datahound import DataProviderBase


table_name = 'test_table'


class DataProvider(DataProviderBase):
    relative_path = 'db/tests.sqlite3'
    db_path = f'{os.path.dirname(os.path.abspath(__file__))}/{relative_path}'

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
        sql = f'create table if not exists {table_name} (' \
            'id integer not null primary key autoincrement, ' \
            'name varchar(32) not null)'
        dataProvider.execute(sql)

    @staticmethod
    def cleanup():
        dataProvider = DataProvider()
        sql = f'drop table {table_name}'
        dataProvider.execute(sql)

    @staticmethod
    def truncateTable(table):
        dataProvider = DataProvider()
        sql = f'delete from {table}'
        dataProvider.execute(sql)

class DataProviderBaseTest(unittest.TestCase):
    def test_connection_error(self):
        sql = f'select * from {table_name}'
        provider = FalseProvider()
        self.assertRaises(Exception, lambda: provider.execute(sql))

    def test_executeCreate(self):
        Helper.setup()
        dataProvider = DataProvider()

        sql = f"select name from sqlite_master where type='table' and name='{table_name}'"
        actual = dataProvider.fetchall(sql)
        self.assertGreater(len(actual), 0)

    def test_executeInsertTruncate(self):
        Helper.truncateTable(table_name)
        sql = f"insert into {table_name} (name) values ('datatest1')"
        dataProvider = DataProvider()
        dataProvider.execute(sql)

        actual_sql = f'select * from {table_name}'
        actual = dataProvider.fetchall(actual_sql)
        self.assertGreater(len(actual), 0)
        self.assertEqual(actual[0][1], 'datatest1')
        Helper.truncateTable(table_name)
        cleaned = dataProvider.fetchall(actual_sql)
        self.assertEqual(len(cleaned), 0)

    def test_fetchall(self):
        Helper.truncateTable(table_name)
        sql = f"insert into {table_name} (name) values ('booger'), ('testing')"
        dataProvider = DataProvider()
        dataProvider.execute(sql)

        actual_sql = f'select * from {table_name}'
        actual = dataProvider.fetchall(actual_sql)
        self.assertEqual(len(actual), 2)
        Helper.truncateTable(table_name)
        self.assertEqual(len(dataProvider.fetchall(actual_sql)), 0)

    def test_fetchmany(self):
        sql = f"insert into {table_name} (name) values ('boogers'), ('boogers1'), ('boogers3'), ('boogers4')"
        dataProvider = DataProvider()
        dataProvider.execute(sql)

        actual_sql = f"select * from {table_name} where name like '%boogers%'"
        actual = dataProvider.fetchmany(3, actual_sql)
        self.assertEqual(len(actual), 3)
        Helper.truncateTable(table_name)

    def test_fetchone(self):
        sql = f"insert into {table_name} (name) values ('fetchone')"
        dataProvider = DataProvider()
        dataProvider.execute(sql)

        actual_sql = f'select * from {table_name} limit 1'
        actual = dataProvider.fetchone(actual_sql)
        self.assertIsNotNone(actual)
        Helper.truncateTable(table_name)
        self.assertIsNone(dataProvider.fetchone(actual_sql))

    def test_execute_scripts(self):
        sql = f"create table if not exists {table_name} (id integer not null primary key autoincrement," \
              f" name varchar(64) not null); insert into {table_name} (name) values ('testing1'), ('testing2')"
        dataProvider = DataProvider()
        dataProvider.execute_scripts(sql)

        actual_sql = f'select * from {table_name}'
        actual = dataProvider.fetchall(actual_sql)
        self.assertIsNotNone(actual)
        self.assertEqual(len(actual), 2)
        dataProvider.execute(f'drop table {table_name}')

    def test_execute_scripts_fail(self):
        sql = f"create table if not exists {table_name} (id integer not null primary key autoincrement," \
              " name varchar(64) not null)"
        dataProvider = DataProvider()
        self.assertRaises(Exception, lambda: dataProvider.execute_scripts(sql))

    def test_fetchallwithparameters(self):
        dataProvider = DataProvider()
        sql = f'insert into {table_name} (name) values (?), (?)'
        dataProvider.execute(sql, 'test1', 'test2')

        actual_sql = f'select name from {table_name} where name = ?'
        actual = dataProvider.fetchall(actual_sql, 'test1')
        self.assertEqual(len(actual), 1)
        self.assertEqual([('test1',)], actual)
        Helper.truncateTable(table_name)

    def test_executereturnid(self):
        Helper.setup()
        dataProvider = DataProvider()
        sql = f'insert into {table_name} (name) values (?)'
        last_id = dataProvider.execute_return_id(sql, 'testing')

        self.assertTrue(type(last_id) == int)
        Helper.truncateTable(table_name)

    def test_executereturnid_deprecation(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter('always')
            Helper.setup()
            dataProvider = DataProvider()
            sql = f'insert into {table_name} (name) values (?)'
            dataProvider.execute_return_id(sql, 'testing')

            self.assertTrue(len(warning) != 0)
            self.assertTrue(issubclass(warning[-1].category, DeprecationWarning))

    def test_insertreturnid(self):
        Helper.setup()
        dataProvider = DataProvider()
        sql = f'insert into {table_name} (name) values (?)'
        last_id = dataProvider.insert_return_id(sql, 'testing')

        self.assertTrue(type(last_id) == int)
        Helper.truncateTable(table_name)

    def test_insertreturnid_fail(self):
        Helper.setup()
        dataProvider = DataProvider()
        sql = f"update {table_name} set name = 'test' where id = 1"

        self.assertRaises(Exception, lambda: dataProvider.insert_return_id(sql))

    def test_insertmany(self):
        dataProvider = DataProvider()
        sql = f'INSERT INTO {table_name} (name) VALUES (?)'
        parameters = ('Test1',), ('Test2',), ('Test3',)
        dataProvider.insert_many(sql, *parameters)

        sql = f'SELECT name FROM {table_name} WHERE name IN (\'Test1\', \'Test2\', \'Test3\')'
        records = dataProvider.fetchall(sql)

        for record in records:
            self.assertTrue(record in parameters)

        Helper.truncateTable(table_name)

    def test_insertmany_fail(self):
        dataProvider = DataProvider()
        sql = f'UPDATE {table_name} SET name = \'Testing\' WHERE id = 0'
        parameters = ('Test1',), ('Test2',), ('Test3',)

        self.assertRaises(Exception, lambda: dataProvider.insert_many(sql, *parameters))
