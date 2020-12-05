import mariadb
import sqlite3

from abc import ABC, abstractmethod

from . import ConnectionString


class _ConnectorBase(ABC):
    @abstractmethod
    def get(self, connection_string: ConnectionString):
        pass


class MariaDbConnector(_ConnectorBase):
    def get(self, connection_string: ConnectionString):
        return mariadb.connect(
            user=connection_string.user_name,
            password=connection_string.password,
            host=connection_string.host,
            port=connection_string.port
        )


class SqLite3Connector(_ConnectorBase):
    def get(self, connection_string: ConnectionString):
        return sqlite3.connect(connection_string.database_path)
