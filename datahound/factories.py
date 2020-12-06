from . import ConnectionString as _ConnectionString
from .connectors import MariaDbConnector as _MariaDbConnector, SqLite3Connector as _SqLite3Connector
from .exceptions import ConnectorException as _ConnectorException
from .managers import DatabaseType as _DatabaseType


class ConnectionFactory(object):
    @staticmethod
    def get_connection(connection_string: _ConnectionString):
        if connection_string.database_type is _DatabaseType.SQLITE:
            return _SqLite3Connector.get_connection(connection_string)
        elif connection_string.database_type is _DatabaseType.MARIADB:
            return _MariaDbConnector.get_connection(connection_string)
        raise _ConnectorException(f'Database Type {connection_string.database_type} is not supported')
