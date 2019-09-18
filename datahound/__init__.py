import sqlite3

from deprecateme import deprecated


class DataProviderBase(object):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        try:
            connection = sqlite3.connect(self.db_path)
            return connection
        except Exception as err:
            raise err

    def fetchall(self, sql: str, *parameters) -> list:
        """Fetches all records that match the supplied query."""
        connection = self._get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, parameters)
        results = cursor.fetchall()

        connection.close()
        return results

    def fetchmany(self, amount: int, sql: str, *parameters) -> list:
        """Fetches the request amount of records that match the supplied query."""
        connection = self._get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, parameters)
        results = cursor.fetchmany(amount)

        connection.close()
        return results

    def fetchone(self, sql: str, *parameters) -> tuple:
        """Fetches one record that match the supplied query."""
        connection = self._get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, parameters)
        result = cursor.fetchone()

        connection.close()
        return result

    def execute(self, sql: str, *parameters) -> None:
        """Executes a query against a database."""
        connection = self._get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, parameters)
        connection.commit()
        connection.close()

    def execute_scripts(self, sql: str) -> None:
        """Executes multiple queries against a database."""
        if ';' not in sql:
            raise AttributeError('This method should be used to run multiple sql statements separated by a semi colon. '
                                 'If you only need to run one script use the execute method instead.')

        connection = self._get_connection()
        cursor = connection.cursor()

        cursor.executescript(sql)
        connection.commit()
        connection.close()

    def insert_return_id(self, sql: str, *parameters) -> int:
        """Inserts a record and returns the primary key value of the record inserted."""
        split_sql = sql.split(' ')

        if split_sql[0].lower() != 'insert':
            raise AttributeError('The sql statement must be an insert statement')

        connection = self._get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, parameters)
        connection.commit()
        returned_id = cursor.lastrowid

        connection.close()
        return returned_id

    def insert_many(self, sql: str, *parameters) -> None:
        """Inserts multiple records in a table with a single sql query."""
        split_sql = sql.split(' ')

        if split_sql[0].lower() != 'insert':
            raise AttributeError('The sql statement must be an insert statement')

        connection = self._get_connection()
        cursor = connection.cursor()

        cursor.executemany(sql, parameters)
        connection.commit()

    @deprecated('This method is deprecated. It will be removed in an upcoming version. '
                'Please use "insert_return_id" instead.')
    def execute_return_id(self, sql: str, *parameters) -> int:
        """Inserts a record and returns the primary key value of the record inserted. (Deprecated)"""
        connection = self._get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, parameters)
        connection.commit()
        returned_id = cursor.lastrowid

        connection.close()
        return returned_id
