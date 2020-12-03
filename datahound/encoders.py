import json


class DatahoundEncoder(json.JSONEncoder):
    """
    Json encoder for datahound. Objects passed through  this encoder must have a to_dict method
    that returns a dictionary.
    """
    def default(self, obj):
        if isinstance(obj, list):
            data = []
            for item in obj:
                data.append(item.to_dict())
            return data
        return obj.to_dict()
