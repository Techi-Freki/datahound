import unittest
import os

from datahound import DataProviderBase
from datahound import ConnectionString
from datahound import DatabaseType


# TODO: Fix tests for both sqlite and mariadb

table_name: str = 'test_table'

sqlite_connection = ConnectionString(DatabaseType.SQLITE,
                                     database_path=f'{os.path.dirname(os.path.abspath(__file__))}/db/tests.sqlite3')

mariadb_connection = ConnectionString(DatabaseType.MARIADB,
                                      user='cms_user',
                                      password='cms_pass',
                                      host='127.0.0.1',
                                      port=3307,
                                      database_name='cms_test'
                                      )

failed_connection = ConnectionString(DatabaseType.SQLITE,
                                     database_path=f'{os.path.dirname(os.path.abspath(__file__))}/db/error_db.txt')

providers = [sqlite_connection, mariadb_connection]


class SqLiteProvider(DataProviderBase):
    def __init__(self):
        super().__init__(sqlite_connection)


class FalseProvider(DataProviderBase):
    db_path = 'db/error_db.txt'

    def __init__(self):
        super().__init__(failed_connection)


class Helper(object):
    @staticmethod
    def setup():
        data_provider = SqLiteProvider()
        sql = f'create table if not exists {table_name} (' \
            'id integer not null primary key autoincrement, ' \
            'name varchar(32) not null)'
        data_provider.execute(sql)

    @staticmethod
    def cleanup():
        data_provider = SqLiteProvider()
        sql = f'drop table {table_name}'
        data_provider.execute(sql)

    @staticmethod
    def truncate_table(table):
        data_provider = SqLiteProvider()
        sql = f'delete from {table}'
        data_provider.execute(sql)


class DataProviderBaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Helper.setup()

    @classmethod
    def tearDownClass(cls):
        Helper.cleanup()

    def test_connection_error(self):
        sql = f'select * from {table_name}'
        provider = FalseProvider()
        self.assertRaises(Exception, lambda: provider.execute(sql))

    def test_executeCreate(self):
        Helper.setup()
        data_provider = SqLiteProvider()

        sql = f"select name from sqlite_master where type='table' and name='{table_name}'"
        actual = data_provider.fetchall(sql)
        self.assertGreater(len(actual), 0)

    def test_executeInsertTruncate(self):
        Helper.setup()
        sql = f"insert into {table_name} (name) values ('datatest1')"
        data_provider = SqLiteProvider()
        data_provider.execute(sql)

        actual_sql = f'select * from {table_name}'
        actual = data_provider.fetchall(actual_sql)
        self.assertGreater(len(actual), 0)
        self.assertEqual(actual[0][1], 'datatest1')
        Helper.truncate_table(table_name)
        cleaned = data_provider.fetchall(actual_sql)
        self.assertEqual(len(cleaned), 0)

    def test_fetchall(self):
        Helper.setup()
        sql = f"insert into {table_name} (name) values ('booger'), ('testing')"
        data_provider = SqLiteProvider()
        data_provider.execute(sql)

        actual_sql = f'select * from {table_name}'
        actual = data_provider.fetchall(actual_sql)
        self.assertEqual(len(actual), 2)
        Helper.truncate_table(table_name)
        self.assertEqual(len(data_provider.fetchall(actual_sql)), 0)

    def test_fetchmany(self):
        Helper.setup()
        sql = f"insert into {table_name} (name) values ('boogers'), ('boogers1'), ('boogers3'), ('boogers4')"
        data_provider = SqLiteProvider()
        data_provider.execute(sql)

        actual_sql = f"select * from {table_name} where name like '%boogers%'"
        actual = data_provider.fetchmany(3, actual_sql)
        self.assertEqual(len(actual), 3)
        Helper.truncate_table(table_name)

    def test_fetchone(self):
        Helper.setup()
        sql = f"insert into {table_name} (name) values ('fetchone')"
        data_provider = SqLiteProvider()
        data_provider.execute(sql)

        actual_sql = f'select * from {table_name} limit 1'
        actual = data_provider.fetchone(actual_sql)
        self.assertIsNotNone(actual)
        Helper.truncate_table(table_name)
        self.assertIsNone(data_provider.fetchone(actual_sql))

    def test_execute_scripts(self):
        sql = f"create table if not exists {table_name} (id integer not null primary key autoincrement," \
              f" name varchar(64) not null); insert into {table_name} (name) values ('testing1'), ('testing2')"
        data_provider = SqLiteProvider()
        data_provider.execute_scripts(sql)

        actual_sql = f'select * from {table_name}'
        actual = data_provider.fetchall(actual_sql)
        self.assertIsNotNone(actual)
        self.assertEqual(len(actual), 2)
        data_provider.execute(f'drop table {table_name}')

    def test_execute_scripts_fail(self):
        Helper.setup()
        sql = f"create table if not exists {table_name} (id integer not null primary key autoincrement," \
              " name varchar(64) not null)"
        data_provider = SqLiteProvider()
        self.assertRaises(Exception, lambda: data_provider.execute_scripts(sql))

    def test_fetchallwithparameters(self):
        Helper.setup()
        data_provider = SqLiteProvider()
        sql = f'insert into {table_name} (name) values (?), (?)'
        data_provider.execute(sql, 'test1', 'test2')

        actual_sql = f'select name from {table_name} where name = ?'
        actual = data_provider.fetchall(actual_sql, 'test1')
        self.assertEqual(len(actual), 1)
        self.assertEqual([('test1',)], actual)
        Helper.truncate_table(table_name)

    def test_insertreturnid(self):
        Helper.setup()
        data_provider = SqLiteProvider()
        sql = f'insert into {table_name} (name) values (?)'
        last_id = data_provider.insert_return_id(sql, 'testing')

        self.assertTrue(type(last_id) == int)
        Helper.truncate_table(table_name)

    def test_insertreturnid_fail(self):
        Helper.setup()
        data_provider = SqLiteProvider()
        sql = f"update {table_name} set name = 'test' where id = 1"

        self.assertRaises(Exception, lambda: data_provider.insert_return_id(sql))

    def test_insertmany(self):
        data_provider = SqLiteProvider()
        sql = f'INSERT INTO {table_name} (name) VALUES (?)'
        parameters = ('Test1',), ('Test2',), ('Test3',)
        data_provider.insert_many(sql, *parameters)

        sql = f'SELECT name FROM {table_name} WHERE name IN (\'Test1\', \'Test2\', \'Test3\')'
        records = data_provider.fetchall(sql)

        for record in records:
            self.assertTrue(record in parameters)

        Helper.truncate_table(table_name)

    def test_insertmany_fail(self):
        data_provider = SqLiteProvider()
        sql = f'UPDATE {table_name} SET name = \'Testing\' WHERE id = 0'
        parameters = ('Test1',), ('Test2',), ('Test3',)

        self.assertRaises(Exception, lambda: data_provider.insert_many(sql, *parameters))
