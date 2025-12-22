# Datahound

![tests](https://github.com/Techi-Freki/datahound/actions/workflows/unit-tests.yaml/badge.svg?event=push)
![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/techi-freki/cb46c7a4cb976b6c148c3c984c7f26d6/raw/coverage.json)

SqLite data access layer for python.

## Methods

* fetchone(sql: str, *parameters) -> tuple
* fetchmany(amount: int, sql: str, *parameters) -> list
* fetchall(sql: str, *parameters) -> list
* insert_return_id(sql: str, *parameters) -> int
* insert_many(sql: str, *parameters) -> None
* execute(sql: str, *parameters) -> None
* execute_scripts(sql: str) -> None

## Usage

### Extending Provider Base

    from datahound import DataProviderBase, ConnectionString


    # add the path to the sqlite db to the connection string object
    sqlite_connection = ConnectionString(database_path='/path/to/db.sqlite')
    sqlite_connection_2 = ConnectionString(database_path='/alt/path/to/db.sqlite')


    # extend the provider base class
    class DataProviderOne(DataProviderBase):
        def __init__(self, connection_string):
            super().__init__(connection_string)


    class DataProviderTwo(DataProviderBase):
        def __init__(self, connection_string):
            super().__init__(connection_string)


    class AppDataProvider(object):
        test_data_one = DataProviderOne(sqlite_connection)
        test_data_two = DataProviderTwo(sqlite_connection_2)

### Running Queries

    def get_data():
        sql = 'SELECT id, name, age FROM user;'
        results = AppDataProvider.test_data_one.fetchall(sql)

        return list(results)


    get_data()
    >> [(1, 'Mark', 25), (2, 'Jane', 31), (3, 'Steve', 45)]

    def return_id(name, age):
        sql = 'INSERT INTO user (name, age) VALUES (?, ?)'
        parameters = (name, age)
        return AppDataProvider.test_data_one.insert_return_id(sql, *parameters)


    return_id('Angela', 27)
    >> 4

    get_data()
    >> [(1, 'Mark', 25), (2, 'Jane', 31), (3, 'Steve', 45), (4, 'Angela', 27)]


### Parameterized Data

    def get_record(id):
        sql = 'SELECT id, name, age FROM user WHERE id = ?'
        result = AppDataProvider.test_data_one.fetchone(sql, id)

        return result


    def insert_record(user):
        sql = 'INSERT INTO user (name, age) VALUES (?, ?)'
        parameters = (user.name, user.age)
        AppDataProvider.test_data_one.execute(sql, *parameters)


    get_record(1)
    >> (1, 'Mark', 25)

### Extensibility

It is now possible to add custom connectors to datahound. Use the entry point group 'datahound.connectors' for adding new database connectors.

See the code in [datahound_mariadb](https://github.com/Techi-Freki/datahound_mariadb) for a better example of how this is accomplished.
