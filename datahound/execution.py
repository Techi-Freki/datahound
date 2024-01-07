from enum import Enum, unique

from .factories import ConnectionFactory


@unique
class _ExecutionType(Enum):
    EXECUTE = 1
    EXECUTE_MANY = 2
    EXECUTE_SCRIPT = 3
    RETURN_ID = 4
    FETCH_ALL = 5
    FETCH_MANY = 6
    FETCH_ONE = 7


class _Executor(object):
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def execute(self, execution_type, sql, *parameters, amount=0):
        if parameters:
            if self._execution_is_fetch(execution_type):
                return self._fetch(execution_type, amount, sql, parameters)
            elif execution_type is _ExecutionType.RETURN_ID:
                return self._execute(execution_type, sql, parameters)
            self._execute(execution_type, sql, parameters)
        else:
            if self._execution_is_fetch(execution_type):
                return self._fetch(execution_type, amount, sql)
            elif execution_type is _ExecutionType.RETURN_ID:
                return self._execute(execution_type, sql)
            self._execute(execution_type, sql)

    def _fetch(self, fetch_type, amount, sql, *parameters) -> list or tuple:
        connection = ConnectionFactory.get_connection(self.connection_string)
        cursor = connection.cursor()
        cursor.execute(sql, *parameters)
        results = None

        if fetch_type is _ExecutionType.FETCH_ALL:
            results = cursor.fetchall()
        elif fetch_type is _ExecutionType.FETCH_MANY:
            results = cursor.fetchmany(amount)
        elif fetch_type is _ExecutionType.FETCH_ONE:
            results = cursor.fetchone()

        connection.close()
        return results

    def _execute(self, execution_type, sql, *parameters) -> int or None:
        connection = ConnectionFactory.get_connection(self.connection_string)
        cursor = connection.cursor()

        if parameters:
            if execution_type is _ExecutionType.EXECUTE_MANY:
                cursor.executemany(sql, *parameters)
            else:
                cursor.execute(sql, *parameters)
        else:
            if execution_type is _ExecutionType.EXECUTE_SCRIPT:
                try:
                    cursor.executescript(sql)
                except:
                    self._executescript(sql, cursor)
            else:
                cursor.execute(sql)

        connection.commit()
        return_id = None

        if execution_type is _ExecutionType.RETURN_ID:
            return_id = cursor.lastrowid

        connection.close()

        if return_id is not None:
            return return_id

    def _execution_is_fetch(self, execution_type: _ExecutionType) -> bool:
        if execution_type is _ExecutionType.FETCH_ALL \
            or execution_type is _ExecutionType.FETCH_MANY \
            or execution_type is _ExecutionType.FETCH_ONE:
            return True
        else:
            return False

    def _executescript(self, sql: str, cursor) -> None:
        sql = sql[:-1] if sql.endswith(';') else sql

        for item in sql.split(';'):
            cursor.execute(item)
