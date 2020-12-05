import sqlite3

from deprecateme import deprecated

from .managers import ExecutionType, Executor


class ConnectionString(object):
    def __init__(self, **kwargs):
        self.database_path = None
        self.database_name = None
        self.user_name = None
        self.password = None
        self.host = None
        self.port = None

        for key, value in kwargs.items():
            if hasattr(ConnectionString, key):
                setattr(ConnectionString, key, value)


class DataProviderBase(object):
    def __init__(self, db_path: str):
        self.db_path = db_path  # TODO: This property will be removed in the next full version.
        self.executor = Executor(db_path)

    def fetchall(self, sql: str, *parameters) -> list:
        """Fetches all records that match the supplied query."""
        return self.executor.execute(ExecutionType.FETCH_ALL, sql, *parameters)

    def fetchmany(self, amount: int, sql: str, *parameters) -> list:
        """Fetches the requested amount of records that match the supplied query."""
        return self.executor.execute(ExecutionType.FETCH_MANY, sql, *parameters, amount=amount)

    def fetchone(self, sql: str, *parameters) -> tuple:
        """Fetches one record that match the supplied query."""
        return self.executor.execute(ExecutionType.FETCH_ONE, sql, *parameters)

    def execute(self, sql: str, *parameters) -> None:
        """Executes a query against a database."""
        self.executor.execute(ExecutionType.EXECUTE, sql, *parameters)

    def execute_scripts(self, sql: str) -> None:
        """Executes multiple queries against a database."""
        if ';' not in sql:
            raise AttributeError('This method should be used to run multiple sql statements separated by a semi colon. '
                                 'If you only need to run one script use the execute method instead.')
        self.executor.execute(ExecutionType.EXECUTE_SCRIPT, sql)

    def insert_return_id(self, sql: str, *parameters) -> int:
        """Inserts a record and returns the primary key value of the record inserted."""
        split_sql = sql.split(' ')

        if split_sql[0].lower() != 'insert':
            raise AttributeError('The sql statement must be an insert statement')
        return self.executor.execute(ExecutionType.RETURN_ID, sql, *parameters)

    def insert_many(self, sql: str, *parameters) -> None:
        """Inserts multiple records in a table with a single sql query."""
        split_sql = sql.split(' ')

        if split_sql[0].lower() != 'insert':
            raise AttributeError('The sql statement must be an insert statement')
        return self.executor.execute(ExecutionType.EXECUTE_MANY, sql, *parameters)

    @deprecated('This method is deprecated. It will be removed in the next full version. '
                'Please use "insert_return_id" instead.')
    def execute_return_id(self, sql: str, *parameters) -> int:
        """Inserts a record and returns the primary key value of the record inserted."""
        connection = self._get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, parameters)
        connection.commit()
        returned_id = cursor.lastrowid

        connection.close()
        return returned_id

    @deprecated('This method is deprecated. It will be removed in the next full version.')
    def _get_connection(self) -> sqlite3.Connection:
        try:
            connection = sqlite3.connect(self.db_path)
            return connection
        except Exception as err:
            raise err
