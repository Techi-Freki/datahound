import mariadb

from abc import ABC, abstractmethod


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


class _ConnectorBase(ABC):
    @abstractmethod
    def get(self, connection_string: ConnectionString):
        pass


class MariaDbConnector(_ConnectorBase):
    def get(self, connection_string: ConnectionString):
        conn = mariadb.connect(
            user=connection_string.user_name,
            password=connection_string.password,
            host=connection_string.host,
            port=connection_string.port
        )

        return conn
