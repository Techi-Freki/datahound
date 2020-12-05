from abc import ABC, abstractmethod


class ConnectorBase(ABC):
    @abstractmethod
    def get(self, database_name, user_name=None, password=None, host=None, port=None):
        pass
