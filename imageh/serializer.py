from enum import Enum
import json


class SerializerJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Enum):
            return o.name
        return json.JSONEncoder.default(self, o)


class Serializer(object):

    def json(self):
        return json.dumps(self.__dict__, sort_keys=True, cls=SerializerJSONEncoder)


