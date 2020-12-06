import mariadb
import sqlite3

from abc import ABC, abstractmethod


class _ConnectorBase(ABC):
    @staticmethod
    @abstractmethod
    def get_connection(connection_string):
        pass


class MariaDbConnector(_ConnectorBase):
    @staticmethod
    def get_connection(connection_string):
        return mariadb.connect(
            user=connection_string.user,
            password=connection_string.password,
            host=connection_string.host,
            port=connection_string.port,
            database=connection_string.database_name
        )


class SqLite3Connector(_ConnectorBase):
    @staticmethod
    def get_connection(connection_string):
        return sqlite3.connect(connection_string.database_path)
