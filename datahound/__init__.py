import sqlite3

from deprecateme import deprecated


class DataProviderBase(object):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def __get_connection(self) -> sqlite3.Connection:
        try:
            connection = sqlite3.connect(self.db_path)
            return connection
        except Exception as err:
            raise err

    def fetchall(self, sql: str, *parameters) -> list:
        connection = self.__get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, parameters)
        results = cursor.fetchall()

        connection.close()
        return results

    def fetchone(self, sql: str, *parameters) -> tuple:
        connection = self.__get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, parameters)
        result = cursor.fetchone()

        connection.close()
        return result

    def execute(self, sql: str, *parameters) -> None:
        connection = self.__get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, parameters)
        connection.commit()
        connection.close()

    def insert_return_id(self, sql: str, *parameters) -> int:
        connection = self.__get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, parameters)
        connection.commit()
        returned_id = cursor.lastrowid

        connection.close()
        return returned_id

    @deprecated('This method is deprecated. It will be removed in an upcoming version. '
                'Please use "insert_return_id" instead.')
    def execute_return_id(self, sql: str, *parameters) -> int:
        connection = self.__get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, parameters)
        connection.commit()
        returned_id = cursor.lastrowid

        connection.close()
        return returned_id
