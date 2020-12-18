from .execution import _ExecutionType, _Executor


class ConnectionString(object):
    def __init__(self, connector_name: str or None = None, **kwargs):
        self.database_path = None
        self.database_name = None
        self.user = None
        self.password = None
        self.host = None
        self.port = None
        self.driver = None
        self.connector_name = connector_name

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class DataProviderBase(object):
    def __init__(self, connection_string: ConnectionString):
        self.connection_string = connection_string
        self.executor = _Executor(connection_string)

    def fetchall(self, sql: str, *parameters) -> list:
        """Fetches all records that match the supplied query."""
        return self.executor.execute(_ExecutionType.FETCH_ALL, sql, *parameters)

    def fetchmany(self, amount: int, sql: str, *parameters) -> list:
        """Fetches the requested amount of records that match the supplied query."""
        return self.executor.execute(_ExecutionType.FETCH_MANY, sql, *parameters, amount=amount)

    def fetchone(self, sql: str, *parameters) -> tuple:
        """Fetches one record that match the supplied query."""
        return self.executor.execute(_ExecutionType.FETCH_ONE, sql, *parameters)

    def execute(self, sql: str, *parameters) -> None:
        """Executes a query against a database."""
        self.executor.execute(_ExecutionType.EXECUTE, sql, *parameters)

    def execute_scripts(self, sql: str) -> None:
        """Executes multiple queries against a database."""
        if ';' not in sql:
            raise AttributeError('This method should be used to run multiple sql statements separated by a semi colon. '
                                 'If you only need to run one script use the execute method instead.')
        self.executor.execute(_ExecutionType.EXECUTE_SCRIPT, sql)

    def insert_return_id(self, sql: str, *parameters) -> int:
        """Inserts a record and returns the primary key value of the record inserted."""
        split_sql = sql.split(' ')

        if split_sql[0].lower() != 'insert':
            raise AttributeError('The sql statement must be an insert statement')
        return self.executor.execute(_ExecutionType.RETURN_ID, sql, *parameters)

    def insert_many(self, sql: str, *parameters) -> None:
        """Inserts multiple records in a table with a single sql query."""
        split_sql = sql.split(' ')

        if split_sql[0].lower() != 'insert':
            raise AttributeError('The sql statement must be an insert statement')
        return self.executor.execute(_ExecutionType.EXECUTE_MANY, sql, *parameters)
