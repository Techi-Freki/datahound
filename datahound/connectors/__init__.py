import sqlite3

from abc import ABC, abstractmethod


class ConnectorBase(ABC):
    @staticmethod
    @abstractmethod
    def get_connection(connection_string):
        pass


class SqLite3Connector(ConnectorBase):
    @staticmethod
    def get_connection(connection_string):
        return sqlite3.connect(connection_string.database_path)
