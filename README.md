# Datahound

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
    sqlite_connection_2 = ConnectionString(database-path='/alt/path/to/db.sqlite')
    
    
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

See the code in [datahound_mariadb](https://python.dbcombs.com/simple/datahound_mariadb) for a better example of how this is accomplished.

## Changelog

2.0.2
* Bug fix

2.0.1
* Added driver property to the connection string object.

2.0.0
* Added database connector plugin support.
* Removed encoder support from 1.1.2.
* Removed deprecated functionality.

1.1.2
* Added an encoder module with a DatahoundEncoder class.

1.1.1

* Refactored code to improve performance and comply with PEP.
* Updated README.md formatting.

1.1.0

* Added **insert_many** and **execute_scripts** to methods.
* Updated README.md and cleaned up private method in package.

1.0.2

* Added **insert_return_id** and deprecated **execute_return_id** due to readability issues.
* Removed extra space in the setup.py file.

1.0.1

* Added MANIFEST.in and updated setup.py.
* Updated README.md to give clearer sql statements in the usage section.

1.0.0

* Added **execute_return_id** method, a method that returns the last inserted id after a successful insert.

1.0.0RC1

* Initial Release.
