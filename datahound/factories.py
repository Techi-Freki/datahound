from enum import Enum, unique

from .connectors import MariaDbConnector as _MariaDbConnector, _SqLite3Connector as _SqLite3Connector
from .exceptions import ConnectorException as _ConnectorException


# TODO: Add more db types for version 2.1.0
@unique
class DatabaseType(Enum):
    SQLITE = 1
    MARIADB = 2


class ConnectionFactory(object):
    @staticmethod
    def get_connection(connection_string):
        if connection_string.database_type is DatabaseType.SQLITE:
            return _SqLite3Connector.get_connection(connection_string)
        elif connection_string.database_type is DatabaseType.MARIADB:
            return _MariaDbConnector.get_connection(connection_string)
        raise _ConnectorException(f'Database Type {connection_string.database_type} is not supported')
