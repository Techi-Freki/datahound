import sqlite3
from enum import Enum, unique


@unique
class ExecutionType(Enum):
    EXECUTE = 1
    EXECUTE_MANY = 2
    EXECUTE_SCRIPT = 3
    RETURN_ID = 4
    FETCH_ALL = 5
    FETCH_MANY = 6
    FETCH_ONE = 7


# TODO: Make datahound database agnostic for version 2.0.0
@unique
class DatabaseType(Enum):
    SQLITE = 1
    MARIADB = 2
    MSSQL = 3
    ETC = 4


class Executor(object):
    def __init__(self, db_path):
        self.db_path = db_path

    def execute(self, execution_type, sql, *parameters, amount=0):
        if parameters:
            if self._execution_is_fetch(execution_type):
                return self._fetch(execution_type, amount, sql, parameters)
            elif execution_type is ExecutionType.RETURN_ID:
                return self._execute(execution_type, sql, parameters)
            self._execute(execution_type, sql, parameters)
        else:
            if self._execution_is_fetch(execution_type):
                return self._fetch(execution_type, amount, sql)
            elif execution_type.name is ExecutionType.RETURN_ID:
                return self._execute(execution_type, sql)
            self._execute(execution_type, sql)

    def _fetch(self, fetch_type, amount, sql, *parameters) -> list or tuple:
        connection = _ConnectionManager.get_connection(self.db_path)
        cursor = connection.cursor()
        cursor.execute(sql, *parameters)
        results = None

        if fetch_type is ExecutionType.FETCH_ALL:
            results = cursor.fetchall()
        elif fetch_type is ExecutionType.FETCH_MANY:
            results = cursor.fetchmany(amount)
        elif fetch_type is ExecutionType.FETCH_ONE:
            results = cursor.fetchone()

        connection.close()
        return results

    def _execute(self, execution_type, sql, *parameters) -> int or None:
        connection = _ConnectionManager.get_connection(self.db_path)
        cursor = connection.cursor()

        if parameters:
            if execution_type is ExecutionType.EXECUTE_MANY:
                cursor.executemany(sql, *parameters)
            else:
                cursor.execute(sql, *parameters)
        else:
            if execution_type.name is ExecutionType.EXECUTE_SCRIPT:
                cursor.executescript(sql)
            else:
                cursor.execute(sql)

        connection.commit()
        return_id = None

        if execution_type.name is ExecutionType.RETURN_ID:
            return_id = cursor.lastrowid

        connection.close()

        if return_id is not None:
            return return_id

    def _execution_is_fetch(self, execution_type: ExecutionType) -> bool:
        if execution_type is ExecutionType.FETCH_ALL \
            or execution_type is ExecutionType.FETCH_MANY \
            or execution_type is ExecutionType.FETCH_ONE:
            return True
        else:
            return False


class _ConnectionManager(object):
    @staticmethod
    def get_connection(db_path: str) -> sqlite3.Connection:
        return sqlite3.connect(db_path)
