import importlib.metadata

from .exceptions import ConnectorException as _ConnectorException


class ConnectionFactory(object):
    @staticmethod
    def get_connection(connection_string):
        entry_point = ConnectionFactory._get_connector_by_name(connection_string.connector_name or 'datahound_sqlite')
        connector = entry_point.load()

        try:
            return connector.get_connection(connection_string)
        except Exception:
            raise _ConnectorException(f'A connector named {connection_string.connector_name} could not be found.')

    @staticmethod
    def _get_connector_by_name(connector_name: str):
        connectors = importlib.metadata.entry_points()['datahound.connectors']

        for connector in connectors:
            if connector.name == connector_name:
                return connector
