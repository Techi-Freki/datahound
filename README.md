#Datahound

SqLite data access layer for python.

##Methods

* fetchone(sql: str, *args) -> tuple
* fetchmany(amount: int, sql: str, *args) -> list
* fetchall(sql: str, *args) -> list
* insert_return_id(sql: str, *args) -> int
* insert_many(sql: str, *args) -> None
* execute(sql: str, *args) -> None
* execute_scripts(sql: str) -> None
* execute_return_id(sql: str, *args) -> int (deprecated)

##Usage

###Extending Provider Base

    from datahound import DataProviderBase
    
    
    # extend the provider base class
    class DataProvider(DataProviderBase):
        db_path = '/path/to/database/test.db'
        
        def __init__(self):
            super().__init__(DataProvider.db_path)
    
    
    class SiteDataProvider(object):
        test_data = new DataProvider()
    
###Running Queries

    def get_data():
        sql = 'SELECT id, name, age FROM user;'
        results = SiteDataProvider.test_data.fetchall(sql)
        
        return list(results)
    
    
    get_data()
    >> [(1, 'Mark', 25), (2, 'Jane', 31), (3, 'Steve', 45)]
    
    def return_id(name, age):
        sql = 'INSERT INTO user (name, age) VALUES (?, ?)'
        parameters = (name, age)
        return SiteDataProvider.test_data.insert_return_id(sql, *parameters)
    
    
    return_id('Angela', 27)
    >> 4
    
    get_data()
    >> [(1, 'Mark', 25), (2, 'Jane', 31), (3, 'Steve', 45), (4, 'Angela', 27)]
    
    
###Parameterized Data
    
    def get_record(id):
        sql = 'SELECT id, name, age FROM user WHERE id = ?'
        result = SiteDataProvider.test_data.fetchone(sql, id)
        
        return result


    def insert_record(user):
        sql = 'INSERT INTO user (name, age) VALUES (?, ?)'
        parameters = (user.name, user.age)
        SiteDataProvider.test_data.execute(sql, *parameters)
        
        
    get_record(1)
    >> (1, 'Mark', 25)

##Changelog

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