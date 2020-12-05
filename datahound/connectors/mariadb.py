import mariadb

from . import ConnectorBase


class MariaDbConnector(ConnectorBase):
    def get(self, database_name, user_name=None, password=None, host=None, port=None):
        conn = mariadb.connect(
            user=user_name,
            password=password,
            host=host,
            port=port
        )

        return conn
