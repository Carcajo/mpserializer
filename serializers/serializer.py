from serializers.parsers.parser_factory_method import create_parser
from serializers.serialization import serialize, deserialize


class Serializer:
    def __init__(self, parser_name):
        self.parser = create_parser(parser_name)

    def dump(self, obj, fp):
        try:
            serialized = serialize(obj)
        except Exception:
            raise ValueError("object can not be serialized")

        try:
            dumped = self.parser.dump(serialized, fp)
        except Exception:
            raise ValueError("serialized object can not be parsed")

        return dumped
        # self.parser.dump(serialize(obj), fp)

    def dumps(self, obj):
        try:
            serialized = serialize(obj)
        except Exception:
            raise ValueError("object can not be serialized")

        try:
            dumped = self.parser.dumps(serialized)
        except Exception:
            raise ValueError("serialized object can not be parsed")

        return dumped
        # return self.parser.dumps(serialize(obj))

    def load(self, fp):
        try:
            loaded = self.parser.load(fp)
        except Exception:
            raise ValueError("file can not be parsed")

        try:
            deserialized = deserialize(loaded)
        except Exception:
            raise ValueError("file can not be deserialized")

        return deserialized
        # return deserialize(self.parser.load(fp))

    def loads(self, s):
        try:
            loaded = self.parser.loads(s)
        except Exception:
            raise ValueError("file can not be parsed")

        try:
            deserialized = deserialize(loaded)
        except Exception:
            raise ValueError("file can not be deserialized")

        return deserialized
        # return deserialize(self.parser.loads(s))
