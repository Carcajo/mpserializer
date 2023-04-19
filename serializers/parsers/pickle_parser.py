import pickle


class PickleParser:
    def dumps(self, obj):
        return pickle.dumps(obj)

    def dump(self, obj, fp):
        fp.write(pickle.dumps(obj))

    def loads(self, s):
        return pickle.loads(s)

    def load(self, fp):
        return pickle.load(fp)
