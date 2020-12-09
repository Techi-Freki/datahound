import importlib.metadata

from .exceptions import ConnectorException as _ConnectorException


class ConnectionFactory(object):
    @staticmethod
    def get_connection(connection_string):
        entry_point = importlib.metadata.entry_points()['datahound.connectors'][0]
        connector = entry_point.load()
        try:
            return connector.get_connection(connection_string)
        except Exception as e:
            raise _ConnectorException(f'A connector named {connection_string.connector_name} could not be found: {e}')
